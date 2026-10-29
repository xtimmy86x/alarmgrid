"""Persistent, bounded Telegram outbox independent of alarm evaluation."""

from __future__ import annotations

import asyncio
import logging
import time
from collections.abc import Awaitable, Callable
from dataclasses import asdict, dataclass
from datetime import timedelta
from typing import Any
from uuid import uuid4

_LOGGER = logging.getLogger(__name__)
MAX_PENDING = 1000
MAX_AGE_SECONDS = 24 * 60 * 60
SEND_TIMEOUT_SECONDS = 30
# Safe for Telegram group chats too (20 messages/minute); also cap the whole bot.
TARGET_INTERVAL_SECONDS = 3.1
GLOBAL_INTERVAL_SECONDS = 0.05


@dataclass
class NotificationDelivery:
    """One independently retried recipient of a lifecycle event."""

    id: str
    rule_id: str | None
    event_type: str
    priority: str | None
    policy: str
    target: str
    message: str
    interactive: bool
    created_at: float
    attempts: int = 0
    next_attempt_at: float = 0

    @classmethod
    def create(cls, **values: Any) -> NotificationDelivery:
        return cls(id=uuid4().hex, created_at=time.time(), **values)


class DeliveryError(Exception):
    """An error with a safe diagnostic code, never a Telegram URL or message."""

    def __init__(self, code: str, *, permanent: bool = False) -> None:
        super().__init__(code)
        self.code = code
        self.permanent = permanent


def delivery_error_details(error: Exception) -> tuple[str, bool, float | None]:
    """Inspect wrapped HA/Telegram errors without logging their sensitive text."""

    current: BaseException | None = error
    seen: set[int] = set()
    code = type(error).__name__
    permanent = False
    retry_after = None
    while current is not None and id(current) not in seen:
        if isinstance(current, asyncio.CancelledError):
            break  # asyncio.timeout chains cancellation under TimeoutError.
        seen.add(id(current))
        code = type(current).__name__
        if isinstance(current, DeliveryError):
            code, permanent = current.code, current.permanent
        elif type(current).__name__ in {
            "Forbidden",
            "InvalidToken",
            "BadRequest",
            "ChatMigrated",
        }:
            code, permanent = type(current).__name__, True
        value = getattr(current, "retry_after", None)
        if isinstance(value, timedelta):
            value = value.total_seconds()
        if isinstance(value, (int, float)) and value >= 0:
            code, permanent, retry_after = "RetryAfter", False, float(value)
        current = current.__cause__ or current.__context__
    return code, permanent, retry_after


class TelegramOutbox:
    """Save before sending; preserve FIFO and retry recipients independently.

    A crash after Telegram accepts a message but before saving its removal can
    result in a duplicate. Timeouts are likewise ambiguous; retries are bounded.
    """

    def __init__(
        self,
        store: Any,
        send: Callable[[NotificationDelivery], Awaitable[None]],
        skip_reason: Callable[[NotificationDelivery], str | None],
        *,
        now: Callable[[], float] = time.time,
    ) -> None:
        self._store = store
        self._send = send
        self._skip_reason = skip_reason
        self._now = now
        self._pending: list[NotificationDelivery] = []
        self._lock = asyncio.Lock()
        self._delivery_lock = asyncio.Lock()
        self._wake = asyncio.Event()
        self._task: asyncio.Task | None = None
        self._closed = False
        self._dirty = False
        self._target_not_before: dict[str, float] = {}
        self._global_not_before = 0.0
        self._stats: dict[str, Any] = {
            "sent": 0,
            "retried": 0,
            "failed": 0,
            "expired": 0,
            "skipped": 0,
            "last_success_at": None,
            "last_failure_at": None,
            "last_error": None,
        }

    async def async_load(self) -> None:
        """Restore pending deliveries; propagate storage errors to HA setup retry."""
        data = await self._store.async_load() or {}
        self._pending = [
            NotificationDelivery(**item) for item in data.get("pending", [])
        ]
        self._stats.update(
            {
                key: value
                for key, value in data.get("stats", {}).items()
                if key in self._stats
            }
        )
        self._global_not_before = float(data.get("global_not_before", 0))
        self._target_not_before = dict(data.get("target_not_before", {}))
        if self._pending:
            _LOGGER.info("Telegram outbox restored: pending=%s", len(self._pending))

    async def async_enqueue(self, deliveries: list[NotificationDelivery]) -> None:
        """Persist eligible messages, never wait for the Telegram service."""
        if not deliveries:
            return
        async with self._lock:
            for item in deliveries:
                if len(self._pending) >= MAX_PENDING or self._closed:
                    self._failure("outbox_closed" if self._closed else "outbox_full")
                    _LOGGER.error(
                        "Telegram delivery rejected: id=%s rule=%s event=%s target=%s reason=%s",
                        item.id,
                        item.rule_id,
                        item.event_type,
                        item.target,
                        self._stats["last_error"],
                    )
                    continue
                self._pending.append(item)
                _LOGGER.debug(
                    "Telegram queued: id=%s rule=%s event=%s target=%s",
                    item.id,
                    item.rule_id,
                    item.event_type,
                    item.target,
                )
            await self._save()
            self._wake.set()

    def start(
        self, create_task: Callable[..., asyncio.Task] = asyncio.create_task
    ) -> None:
        """Run as an HA background task so startup does not wait for retry timers."""
        if self._task is None:
            self._task = create_task(self._run(), name="AlarmGrid Telegram outbox")

    async def async_close(self) -> None:
        """Stop network work and retain all unfinished deliveries for next setup."""
        self._closed = True
        if self._task is not None:
            self._task.cancel()
            await asyncio.gather(self._task, return_exceptions=True)
            self._task = None
        async with self._lock:
            await self._save()

    def diagnostics(self) -> dict[str, Any]:
        """Expose aggregate outcomes, never targets, tokens, or message bodies."""
        return {
            **self._stats,
            "pending": len(self._pending),
            "storage_dirty": self._dirty,
            "oldest_pending_age_seconds": max(
                0, int(self._now() - min(item.created_at for item in self._pending))
            )
            if self._pending
            else 0,
        }

    def _next(self) -> tuple[NotificationDelivery | None, float]:
        seen: set[str] = set()
        candidates = []
        for item in self._pending:
            if item.target in seen:
                continue
            seen.add(item.target)
            due = max(
                item.next_attempt_at,
                self._target_not_before.get(item.target, 0),
                self._global_not_before,
            )
            # Expiration/settings changes must not wait for a long RetryAfter.
            if self._skip_reason(item):
                due = 0
            candidates.append((min(due, item.created_at + MAX_AGE_SECONDS), item))
        if not candidates:
            return None, 0
        due, item = min(candidates, key=lambda value: value[0])
        return item, due

    async def async_process_once(self) -> bool:
        """Process at most one due delivery (also useful for deterministic tests)."""
        async with self._delivery_lock:
            async with self._lock:
                item, due = self._next()
                if item is None or due > self._now() or self._closed:
                    return False
                reason = self._skip_reason(item)
                if reason or self._now() - item.created_at >= MAX_AGE_SECONDS:
                    self._pending.remove(item)
                    if reason:
                        self._stats["skipped"] += 1
                        _LOGGER.info(
                            "Telegram pending delivery cancelled: id=%s rule=%s target=%s reason=%s",
                            item.id,
                            item.rule_id,
                            item.target,
                            reason,
                        )
                    else:
                        self._stats["expired"] += 1
                        self._failure("expired")
                        _LOGGER.error(
                            "Telegram delivery expired after 24h: id=%s rule=%s event=%s target=%s attempts=%s",
                            item.id,
                            item.rule_id,
                            item.event_type,
                            item.target,
                            item.attempts,
                        )
                    await self._save()
                    return True
                item.attempts += 1
            error = None
            try:
                async with asyncio.timeout(SEND_TIMEOUT_SECONDS):
                    await self._send(item)
            except Exception as err:
                error = err
            async with self._lock:
                now = self._now()
                self._target_not_before[item.target] = now + TARGET_INTERVAL_SECONDS
                self._global_not_before = now + GLOBAL_INTERVAL_SECONDS
                if error is None:
                    self._pending.remove(item)
                    self._stats["sent"] += 1
                    self._stats["last_success_at"] = now
                    _LOGGER.log(
                        logging.INFO if item.attempts > 1 else logging.DEBUG,
                        "Telegram sent: id=%s rule=%s event=%s target=%s attempt=%s",
                        item.id,
                        item.rule_id,
                        item.event_type,
                        item.target,
                        item.attempts,
                    )
                else:
                    code, permanent, retry_after = delivery_error_details(error)
                    self._stats.update(last_error=code, last_failure_at=now)
                    if permanent:
                        self._pending.remove(item)
                        self._stats["failed"] += 1
                        _LOGGER.error(
                            "Telegram delivery failed permanently: id=%s rule=%s event=%s target=%s error=%s; check bot/chat configuration",
                            item.id,
                            item.rule_id,
                            item.event_type,
                            item.target,
                            code,
                        )
                    else:
                        delay = max(
                            min(300, 5 * 2 ** min(item.attempts - 1, 6)),
                            retry_after or 0,
                        )
                        item.next_attempt_at = now + delay
                        if retry_after is not None:
                            self._global_not_before = max(
                                self._global_not_before, now + retry_after
                            )
                        self._stats["retried"] += 1
                        _LOGGER.warning(
                            "Telegram send failed: id=%s rule=%s event=%s target=%s attempt=%s error=%s retry_in=%.1fs",
                            item.id,
                            item.rule_id,
                            item.event_type,
                            item.target,
                            item.attempts,
                            code,
                            delay,
                        )
                await self._save()
            return True

    def _failure(self, code: str) -> None:
        self._stats["failed"] += 1
        self._stats.update(last_failure_at=self._now(), last_error=code)

    async def _save(self) -> None:
        try:
            await self._store.async_save(
                {
                    "pending": [asdict(item) for item in self._pending],
                    "stats": dict(self._stats),
                    "global_not_before": self._global_not_before,
                    "target_not_before": {
                        key: value
                        for key, value in self._target_not_before.items()
                        if value > self._now()
                    },
                }
            )
        except Exception as err:
            self._dirty = True
            _LOGGER.error(
                "Telegram outbox persistence failed: error=%s pending=%s; deliveries remain in memory and may be lost on restart",
                type(err).__name__,
                len(self._pending),
            )
        else:
            if self._dirty:
                _LOGGER.info("Telegram outbox persistence recovered")
            self._dirty = False

    async def _run(self) -> None:
        while not self._closed:
            self._wake.clear()
            if await self.async_process_once():
                continue
            async with self._lock:
                if self._dirty:
                    await self._save()
                item, due = self._next()
                timeout = max(0.01, due - self._now()) if item else None
                if self._dirty:
                    timeout = min(timeout, 30) if timeout is not None else 30
            try:
                await asyncio.wait_for(self._wake.wait(), timeout)
            except TimeoutError:
                pass
