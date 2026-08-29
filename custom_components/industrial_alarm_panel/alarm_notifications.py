"""Best-effort outbound alarm notifications."""

from __future__ import annotations

import logging
from collections.abc import Awaitable, Callable
from typing import Any, Protocol

from .alarm_models import (
    PRIORITY_PROFILES,
    AlarmEvent,
    AlarmEventType,
    AlarmPriority,
    TelegramNotificationPolicy,
)
from .const import (
    CONF_TELEGRAM_ENABLED,
    CONF_TELEGRAM_INTERACTIVE_ENABLED,
    CONF_TELEGRAM_MIN_PRIORITY,
    CONF_TELEGRAM_NOTIFY_ACKNOWLEDGED,
    CONF_TELEGRAM_NOTIFY_ACTIVATED,
    CONF_TELEGRAM_NOTIFY_CLEARED,
    CONF_TELEGRAM_NOTIFY_DISABLED,
    CONF_TELEGRAM_NOTIFY_ENABLED,
    CONF_TELEGRAM_NOTIFY_SHELVED,
    CONF_TELEGRAM_NOTIFY_UNSHELVED,
    CONF_TELEGRAM_TARGETS,
)
from .telegram_i18n import normalize_telegram_language, telegram_text
from .telegram_interactive import TelegramInteractiveManager

_LOGGER = logging.getLogger(__name__)

NotifyCall = Callable[[str, str], Awaitable[None]]

_EVENT_OPTIONS = {
    AlarmEventType.ACTIVATED.value: CONF_TELEGRAM_NOTIFY_ACTIVATED,
    AlarmEventType.CLEARED.value: CONF_TELEGRAM_NOTIFY_CLEARED,
    AlarmEventType.ACKNOWLEDGED.value: CONF_TELEGRAM_NOTIFY_ACKNOWLEDGED,
    AlarmEventType.SHELVED.value: CONF_TELEGRAM_NOTIFY_SHELVED,
    AlarmEventType.UNSHELVED.value: CONF_TELEGRAM_NOTIFY_UNSHELVED,
    AlarmEventType.DISABLED.value: CONF_TELEGRAM_NOTIFY_DISABLED,
    AlarmEventType.ENABLED.value: CONF_TELEGRAM_NOTIFY_ENABLED,
}

_PRIORITY_EMOJI = {
    AlarmPriority.CRITICAL.value: "🔴",
    AlarmPriority.HIGH.value: "🟠",
    AlarmPriority.MEDIUM.value: "🟡",
    AlarmPriority.LOW.value: "🔵",
    AlarmPriority.INFO.value: "ℹ️",
    AlarmPriority.STATUS.value: "🟢",
}

_EVENT_EMOJI = {
    AlarmEventType.CLEARED.value: "✅",
    AlarmEventType.ACKNOWLEDGED.value: "✅",
    AlarmEventType.SHELVED.value: "💤",
    AlarmEventType.UNSHELVED.value: "🔔",
    AlarmEventType.DISABLED.value: "🚫",
    AlarmEventType.ENABLED.value: "▶️",
}


class AlarmNotifier(Protocol):
    """Provider interface kept deliberately small for future channels."""

    async def notify(self, event: AlarmEvent) -> None:
        """Deliver one event."""


class AlarmNotificationManager:
    """Fan alarm events out to independent notification providers."""

    def __init__(self, providers: list[AlarmNotifier] | None = None) -> None:
        self.providers = providers or []

    async def notify(self, event: AlarmEvent) -> None:
        """Notify every provider without affecting alarm processing."""

        for provider in self.providers:
            try:
                await provider.notify(event)
            except Exception:  # Providers are an external best-effort boundary.
                _LOGGER.warning(
                    "Alarm notification provider failed for event %s",
                    event.event_type,
                    exc_info=True,
                )


class TelegramNotifier:
    """Send plain-text messages through Home Assistant notify entities."""

    def __init__(
        self,
        options: dict[str, Any],
        notify_call: NotifyCall,
        interactive_manager: TelegramInteractiveManager | None = None,
        language: str = "en",
    ) -> None:
        self._options = options
        self._notify_call = notify_call
        self._interactive_manager = interactive_manager
        self._language = normalize_telegram_language(language)

    async def notify(self, event: AlarmEvent) -> None:
        """Send a configured lifecycle event to each available target."""

        if not self._options.get(CONF_TELEGRAM_ENABLED, False):
            return
        targets = list(self._options.get(CONF_TELEGRAM_TARGETS) or [])
        event_option = _EVENT_OPTIONS.get(event.event_type)
        if (
            not targets
            or event_option is None
            or not self._options.get(event_option, False)
        ):
            return
        try:
            policy = TelegramNotificationPolicy(
                event.metadata.get(
                    "telegram_notification_policy",
                    TelegramNotificationPolicy.INHERIT.value,
                )
            )
        except ValueError:
            _LOGGER.warning("Invalid Telegram notification policy in alarm event")
            policy = TelegramNotificationPolicy.INHERIT
        if policy == TelegramNotificationPolicy.NEVER:
            return
        if (
            policy == TelegramNotificationPolicy.INHERIT
            and not self._meets_minimum_priority(event.priority)
        ):
            return

        message = format_telegram_message(event, self._language)
        if (
            event.event_type == AlarmEventType.ACTIVATED.value
            and self._options.get(CONF_TELEGRAM_INTERACTIVE_ENABLED, False)
            and self._interactive_manager is not None
        ):
            await self._notify_interactive(event, targets, message)
            return
        for target in targets:
            try:
                await self._notify_call(target, message)
            except Exception:  # One unavailable notify entity must not stop others.
                _LOGGER.warning(
                    "Could not send alarm notification to %s", target, exc_info=True
                )

    async def _notify_interactive(
        self, event: AlarmEvent, targets: list[str], message: str
    ) -> None:
        """Send isolated interactive messages, falling back only on definite failure."""

        manager = self._interactive_manager
        assert manager is not None
        rule = manager.engine.rules.get(event.rule_id)
        for target in targets:
            token = manager.new_token()
            keyboard = manager.keyboard(token, rule)
            try:
                response = await manager.hass.services.async_call(
                    "telegram_bot",
                    "send_message",
                    service_data={"message": message, "inline_keyboard": keyboard},
                    target={"entity_id": target},
                    blocking=True,
                    return_response=True,
                )
            except Exception:
                _LOGGER.warning(
                    "Could not send interactive Telegram alarm notification",
                    exc_info=True,
                )
                try:
                    await self._notify_call(target, message)
                except Exception:
                    _LOGGER.warning(
                        "Telegram plain notification fallback failed", exc_info=True
                    )
                continue
            chat = _extract_sent_chat(response)
            if chat is None:
                _LOGGER.warning(
                    "Interactive Telegram response did not contain message identifiers"
                )
                continue
            manager.add_session(
                token,
                event.rule_id or "",
                target,
                chat["chat_id"],
                chat["message_id"],
                message,
            )

    def _meets_minimum_priority(self, priority: str | None) -> bool:
        if priority is None:
            return False
        try:
            actual = PRIORITY_PROFILES[AlarmPriority(priority)]["severity"]
            minimum = PRIORITY_PROFILES[
                AlarmPriority(self._options.get(CONF_TELEGRAM_MIN_PRIORITY, "high"))
            ]["severity"]
        except (KeyError, ValueError):
            _LOGGER.warning("Invalid Telegram alarm priority configuration")
            return False
        return int(actual) >= int(minimum)


def format_telegram_message(event: AlarmEvent, language: str = "en") -> str:
    """Create a compact, safe plain-text message, omitting empty fields."""

    language = normalize_telegram_language(language)
    priority = telegram_text(language, f"priority_{event.priority}")
    emoji = _EVENT_EMOJI.get(event.event_type) or _PRIORITY_EMOJI.get(
        event.priority or "", "🔔"
    )
    title = event.name or event.tag or event.entity_id or telegram_text(language, "alarm")
    event_label = telegram_text(language, f"event_{event.event_type}")
    lines = [f"{emoji} {event_label} — {title}", ""]
    fields = (
        ("priority", priority), ("area", event.area), ("system", event.system),
        ("tag", event.tag), ("state", event.source_state),
        ("value", event.source_value), ("operator", event.operator),
        ("reason", event.message),
        ("time", event.timestamp.astimezone().strftime("%H:%M")),
    )
    lines.extend(
        f"{telegram_text(language, f'field_{key}')}: {value}"
        for key, value in fields if value not in (None, "")
    )
    return "\n".join(lines)


def _extract_sent_chat(response: Any) -> dict[str, Any] | None:
    """Read HA's response data while tolerating its entity-keyed service wrapper."""

    candidates = [response]
    if isinstance(response, dict):
        candidates.extend(response.values())
    for candidate in candidates:
        if not isinstance(candidate, dict):
            continue
        chats = candidate.get("chats")
        if isinstance(chats, list) and chats and isinstance(chats[0], dict):
            candidate = chats[0]
        if (
            candidate.get("chat_id") is not None
            and candidate.get("message_id") is not None
        ):
            return candidate
    return None
