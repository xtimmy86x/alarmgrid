"""Telegram delivery policy, safe message formatting, and HA transport."""

from __future__ import annotations

import logging
from collections.abc import Awaitable, Callable
from decimal import Decimal, InvalidOperation
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
from .notification_queue import (
    DeliveryError,
    NotificationDelivery,
    TelegramOutbox,
    delivery_error_details,
)
from .telegram_i18n import normalize_telegram_language, telegram_text
from .telegram_interactive import TelegramInteractiveManager

_LOGGER = logging.getLogger(__name__)

NotifyCall = Callable[[str, str], Awaitable[Any]]

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
            except Exception as err:  # Providers are an external best-effort boundary.
                _LOGGER.warning(
                    "Alarm notification provider failed: rule=%s event=%s error=%s",
                    event.rule_id,
                    event.event_type,
                    type(err).__name__,
                )


class TelegramNotifier:
    """Send plain-text messages through Home Assistant notify entities."""

    def __init__(
        self,
        options: dict[str, Any],
        notify_call: NotifyCall,
        interactive_manager: TelegramInteractiveManager | None = None,
        language: str = "en",
        rule_lookup: Callable[[str], Any] | None = None,
    ) -> None:
        self._options = options
        self._notify_call = notify_call
        self._interactive_manager = interactive_manager
        self._language = normalize_telegram_language(language)
        self._rule_lookup = rule_lookup
        self.outbox: TelegramOutbox | None = None

    async def notify(self, event: AlarmEvent) -> None:
        """Enqueue each eligible recipient without performing network I/O."""
        targets = list(dict.fromkeys(self._options.get(CONF_TELEGRAM_TARGETS) or []))
        if not targets:
            _LOGGER.debug(
                "Telegram skipped: rule=%s event=%s reason=no_targets",
                event.rule_id,
                event.event_type,
            )
            return
        deliveries = []
        message = None
        for target in targets:
            item = NotificationDelivery.create(
                rule_id=event.rule_id,
                event_type=event.event_type,
                priority=event.priority,
                policy=event.metadata.get("telegram_notification_policy", "inherit"),
                target=target,
                message="",
                interactive=event.event_type == AlarmEventType.ACTIVATED.value,
            )
            reason = self.skip_reason(item)
            if reason:
                _LOGGER.debug(
                    "Telegram skipped: rule=%s event=%s target=%s reason=%s",
                    event.rule_id,
                    event.event_type,
                    target,
                    reason,
                )
                continue
            if message is None:
                message = format_telegram_message(event, self._language)
            item.message = message
            deliveries.append(item)
        if self.outbox is not None:
            await self.outbox.async_enqueue(deliveries)
            return
        # Standalone use; HA setup always binds the durable outbox.
        for item in deliveries:
            try:
                await self.async_deliver(item)
            except Exception as err:
                _LOGGER.warning(
                    "Telegram send failed: rule=%s event=%s target=%s error=%s",
                    item.rule_id,
                    item.event_type,
                    item.target,
                    delivery_error_details(err)[0],
                )

    def skip_reason(self, item: NotificationDelivery) -> str | None:
        """Apply current settings again when replaying a persisted delivery."""
        if not self._options.get(CONF_TELEGRAM_ENABLED, False):
            return "telegram_disabled"
        if item.target not in (self._options.get(CONF_TELEGRAM_TARGETS) or []):
            return "target_removed"
        event_option = _EVENT_OPTIONS.get(item.event_type)
        if event_option is None:
            return "unsupported_event"
        if not self._options.get(event_option, False):
            return "event_disabled"
        policy = item.policy
        if self._rule_lookup is not None:
            rule = self._rule_lookup(item.rule_id or "")
            if rule is None:
                return "rule_deleted"
            policy = rule.telegram_notification_policy
        if policy == TelegramNotificationPolicy.NEVER:
            return "rule_policy_never"
        if (
            policy != TelegramNotificationPolicy.ALWAYS
            and not self._meets_minimum_priority(item.priority)
        ):
            return "below_minimum_priority"
        return None

    async def async_deliver(self, item: NotificationDelivery) -> None:
        """Perform one attempt; the outbox owns retries and error reporting."""
        manager = self._interactive_manager
        if not (
            item.interactive
            and self._options.get(CONF_TELEGRAM_INTERACTIVE_ENABLED, False)
            and manager is not None
        ):
            await self._notify_call(item.target, item.message)
            return
        rule = manager.engine.rules.get(item.rule_id)
        token = manager.new_token()
        try:
            chat = await async_send_telegram(
                manager.hass,
                item.target,
                item.message,
                keyboard=manager.keyboard(token, rule),
            )
        except Exception as err:
            # Only a rejected keyboard is a definite non-delivery worth an immediate
            # plain fallback. Network timeouts may already have delivered the message.
            if getattr(err, "translation_key", None) != "invalid_inline_keyboard":
                raise
            _LOGGER.warning(
                "Telegram keyboard rejected; sending plain text: rule=%s target=%s",
                item.rule_id,
                item.target,
            )
            await self._notify_call(item.target, item.message)
            return
        manager.add_session(
            token,
            item.rule_id or "",
            item.target,
            chat["chat_id"],
            chat["message_id"],
            item.message,
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


async def async_send_telegram(
    hass: Any, target: str, message: str, *, keyboard: list | None = None
) -> dict[str, Any]:
    """Send literal text through the Telegram action and verify API acceptance."""
    state = hass.states.get(target)
    if state is None or state.state == "unavailable":
        raise DeliveryError("target_unavailable")
    data: dict[str, Any] = {
        "message": truncate_telegram_text(message),
        "parse_mode": "plain_text",
    }
    if keyboard is not None:
        data["inline_keyboard"] = keyboard
    response = await hass.services.async_call(
        "telegram_bot",
        "send_message",
        service_data=data,
        target={"entity_id": target},
        blocking=True,
        return_response=True,
    )
    chat = _extract_sent_chat(response)
    if chat is None:
        raise DeliveryError("missing_message_identifiers")
    return chat


def truncate_telegram_text(value: str, limit: int = 4096) -> str:
    """Bound UTF-16 code units too, without cutting a surrogate pair."""
    encoded = value.encode("utf-16-le")
    if len(encoded) <= limit * 2:
        return value
    return encoded[: (limit - 1) * 2].decode("utf-16-le", errors="ignore") + "…"


def format_telegram_message(event: AlarmEvent, language: str = "en") -> str:
    """Separate status, location and reading without repeating generated text."""

    language = normalize_telegram_language(language)
    emoji = _EVENT_EMOJI.get(event.event_type) or _PRIORITY_EMOJI.get(
        event.priority or "", "🔔"
    )
    full_title = (
        event.name or event.tag or event.entity_id or telegram_text(language, "alarm")
    )
    title = truncate_telegram_text(full_title, 256)
    event_label = telegram_text(language, f"event_{event.event_type}")
    sections = [f"{emoji} {event_label}\n{title}"]

    def section(fields: list[tuple[str, Any]]) -> None:
        lines = [
            f"{telegram_text(language, f'field_{key}')}: {truncate_telegram_text(str(value), 600 if key == 'reason' else 300)}"
            for key, value in fields
            if value not in (None, "")
        ]
        if lines:
            sections.append("\n".join(lines))

    section(
        [
            ("area", event.area),
            ("system", event.system),
            ("tag", event.tag if event.tag != full_title else None),
            (
                "priority",
                telegram_text(language, f"priority_{event.priority}")
                if event.priority
                else None,
            ),
        ]
    )
    presentation = event.metadata.get("telegram_presentation") or {}
    readings = _telegram_readings(event, presentation, language)
    condition = presentation.get("condition")
    # This is the activation condition, not a claim about a cleared reading.
    if event.event_type == AlarmEventType.ACTIVATED.value and condition in {
        "above",
        "below",
        "equal",
        "not_equal",
        "contains",
    }:
        threshold = presentation.get("threshold")
        if threshold is not None:
            readings.append(
                (
                    "condition",
                    telegram_text(language, f"condition_{condition}").format(
                        value=_telegram_value(threshold, language)
                        if condition in {"above", "below"}
                        else f"“{threshold}”",
                    ),
                )
            )
    section(readings)

    reason = (
        presentation.get("description")
        if presentation.get("generated_message")
        else event.message
    )
    section(
        [
            ("operator", event.operator),
            ("reason", reason if reason != full_title else None),
        ]
    )
    time_format = "%d/%m/%Y · %H:%M %Z" if language == "it" else "%Y-%m-%d · %H:%M %Z"
    sections.append(f"🕒 {event.timestamp.astimezone().strftime(time_format)}")
    return truncate_telegram_text("\n\n".join(sections))


def _telegram_value(value: Any, language: str) -> str:
    """Localize typed numbers, preserving text thresholds and their exact values."""
    text = str(value)
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        if text.endswith(".0"):
            text = text[:-2]
        if language == "it":
            text = text.replace(".", ",")
    return text


def _telegram_state(value: Any, language: str) -> str:
    text = str(value)
    if text in {"on", "off", "unavailable", "unknown", "manual"}:
        return telegram_text(language, f"state_{text}")
    return text


def _telegram_readings(
    event: AlarmEvent,
    presentation: dict[str, Any],
    language: str,
) -> list[tuple[str, Any]]:
    """Keep meaningful source differences while collapsing duplicate readings."""
    matched = presentation.get("matched_conditions")
    total = presentation.get("total_conditions")
    if isinstance(matched, int) and isinstance(total, int):
        return [
            (
                "conditions",
                telegram_text(language, "conditions_matched").format(
                    matched=matched,
                    total=total,
                ),
            )
        ]

    state, value = event.source_state, event.source_value
    if value in (None, ""):
        return (
            [("state", _telegram_state(state, language))]
            if state not in (None, "")
            else []
        )
    numeric = isinstance(value, (int, float)) and not isinstance(value, bool)
    same = str(state) == str(value)
    if numeric and state not in (None, ""):
        try:
            same = Decimal(str(state)) == Decimal(str(value))
        except InvalidOperation:
            pass
    if same and not numeric:
        return [("state", _telegram_state(state, language))]
    fields = []
    if state not in (None, "") and not same:
        fields.append(("state", _telegram_state(state, language)))
    fields.append(("value", _telegram_value(value, language)))
    return fields


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
