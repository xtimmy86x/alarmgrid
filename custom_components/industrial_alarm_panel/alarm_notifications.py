"""Best-effort outbound alarm notifications."""

from __future__ import annotations

import logging
from collections.abc import Awaitable, Callable
from typing import Any, Protocol

from .alarm_models import PRIORITY_PROFILES, AlarmEvent, AlarmEventType, AlarmPriority
from .const import (
    CONF_TELEGRAM_ENABLED,
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

    def __init__(self, options: dict[str, Any], notify_call: NotifyCall) -> None:
        self._options = options
        self._notify_call = notify_call

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
        if not self._meets_minimum_priority(event.priority):
            return

        message = format_telegram_message(event)
        for target in targets:
            try:
                await self._notify_call(target, message)
            except Exception:  # One unavailable notify entity must not stop others.
                _LOGGER.warning(
                    "Could not send alarm notification to %s", target, exc_info=True
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


def format_telegram_message(event: AlarmEvent) -> str:
    """Create a compact, safe plain-text message, omitting empty fields."""

    priority = (event.priority or "unknown").upper()
    emoji = _EVENT_EMOJI.get(event.event_type) or _PRIORITY_EMOJI.get(
        event.priority or "", "🔔"
    )
    title = event.name or event.tag or event.entity_id or "Alarm"
    lines = [f"{emoji} {event.event_type.upper()} — {title}", ""]
    fields = (
        ("Priority", priority),
        ("Area", event.area),
        ("System", event.system),
        ("Tag", event.tag),
        ("State", event.source_state),
        ("Value", event.source_value),
        ("Operator", event.operator),
        ("Reason", event.message),
        ("Time", event.timestamp.astimezone().strftime("%H:%M")),
    )
    lines.extend(
        f"{label}: {value}" for label, value in fields if value not in (None, "")
    )
    return "\n".join(lines)
