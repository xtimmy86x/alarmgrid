"""Alarm sound and horn state manager."""

from __future__ import annotations

import logging
from collections.abc import Awaitable, Callable
from datetime import UTC, datetime, timedelta
from typing import Any

from .alarm_models import PRIORITY_PROFILES, AlarmPriority

_LOGGER = logging.getLogger(__name__)

MediaCall = Callable[[str, AlarmPriority], Awaitable[None]]


class AlarmSoundManager:
    """Manage audible alarm state for browser and media-player sound."""

    def __init__(
        self,
        *,
        sound_mode: str = "browser_only",
        repeat_interval_seconds: int = 30,
        repeat_until_silenced: bool = True,
        now: Callable[[], datetime] | None = None,
        media_players: list[str] | None = None,
        media_call: MediaCall | None = None,
    ) -> None:
        self.sound_mode = sound_mode
        self.repeat_interval_seconds = repeat_interval_seconds
        self.repeat_until_silenced = repeat_until_silenced
        self._now = now or (lambda: datetime.now(UTC))
        self.media_players = media_players or []
        self._media_call = media_call
        self.active_audible_alarms: dict[str, AlarmPriority] = {}
        self.horn_active = False
        self.silenced = False
        self.silenced_until: datetime | None = None
        self.last_sound_at: datetime | None = None
        self.test_sound_at: datetime | None = None

    def storage_state(self) -> dict[str, Any]:
        """Persist operator silence together with alarm runtime states."""
        return {
            "silenced": self.silenced,
            "silenced_until": self.silenced_until.isoformat() if self.silenced_until else None,
            "last_sound_at": self.last_sound_at.isoformat() if self.last_sound_at else None,
        }

    def restore_state(
        self, data: dict[str, Any], audible_alarms: dict[str, AlarmPriority]
    ) -> None:
        """Seed known alarms without treating them as new audible activations."""
        def timestamp(key: str) -> datetime | None:
            value = data.get(key)
            if not value:
                return None
            try:
                parsed = datetime.fromisoformat(value)
                return parsed if parsed.tzinfo else parsed.replace(tzinfo=UTC)
            except (TypeError, ValueError):
                return None

        self.silenced = bool(data.get("silenced", False))
        self.silenced_until = timestamp("silenced_until") if self.silenced else None
        self.last_sound_at = timestamp("last_sound_at")
        self.active_audible_alarms = dict(audible_alarms)
        self.horn_active = bool(audible_alarms) and not self.silenced and self.sound_mode != "none"
        if self.horn_active and self.last_sound_at is None:
            self.last_sound_at = self._now()

    @property
    def browser_enabled(self) -> bool:
        """Return whether browser panel sound should be active."""

        return self.sound_mode in {"browser_only", "browser_and_media_player"}

    @property
    def media_player_enabled(self) -> bool:
        """Return whether media player sound should be active."""

        return self.sound_mode in {"media_player_only", "browser_and_media_player"}

    async def on_alarm_requires_sound(
        self, rule_id: str, priority: AlarmPriority
    ) -> None:
        """Start or re-start sound for a new unacknowledged audible alarm."""

        new_alarm = rule_id not in self.active_audible_alarms
        force_sound = new_alarm and (self.silenced or not self.horn_active)
        self.active_audible_alarms[rule_id] = priority
        if self.sound_mode == "none":
            return
        if new_alarm:
            self.silenced = False
            self.silenced_until = None
        if not self.silenced:
            self.horn_active = True
            if force_sound or (new_alarm and not self.repeat_until_silenced) or self._sound_cooldown_elapsed():
                self.last_sound_at = self._now()
                await self._play_media_if_needed(rule_id, priority)

    async def on_alarm_acknowledged(self, rule_id: str) -> None:
        """Remove an alarm from the audible set."""

        self.active_audible_alarms.pop(rule_id, None)
        if not self.active_audible_alarms:
            self.horn_active = False

    async def silence(self, duration_seconds: int | None = None) -> None:
        """Silence the horn without acknowledging alarms."""

        self.horn_active = False
        self.silenced = True
        self.silenced_until = (
            self._now() + timedelta(seconds=duration_seconds)
            if duration_seconds
            else None
        )

    async def unsilence(self) -> None:
        """Unsilence the horn."""

        self.silenced = False
        self.silenced_until = None
        self.horn_active = bool(self.active_audible_alarms) and self.sound_mode != "none"
        if self.horn_active:
            await self._emit_sound()

    async def test_sound(self, priority: AlarmPriority = AlarmPriority.CRITICAL) -> None:
        """Play a one-shot test sound."""

        # A test must not start a permanent horn or disturb an active alarm.
        if self.browser_enabled:
            self.test_sound_at = self._now()
        await self._play_media_if_needed("__test__", priority)

    async def _emit_sound(self) -> None:
        rule_id = max(self.active_audible_alarms, key=lambda key:
                      PRIORITY_PROFILES[self.active_audible_alarms[key]]["severity"])
        self.last_sound_at = self._now()
        await self._play_media_if_needed(rule_id, self.active_audible_alarms[rule_id])

    def next_due_at(self) -> datetime | None:
        """Share the integration timer for repeats and timed silence expiry."""
        if self.sound_mode == "none" or not self.active_audible_alarms:
            return None
        if self.silenced:
            return self.silenced_until
        if self.horn_active and self.repeat_until_silenced and self.last_sound_at:
            return self.last_sound_at + timedelta(seconds=max(1, self.repeat_interval_seconds))
        return None

    async def process_due(self) -> bool:
        due = self.next_due_at()
        if due is None or due > self._now():
            return False
        if self.silenced:
            await self.unsilence()
        else:
            await self._emit_sound()
        return True

    async def _play_media_if_needed(
        self, rule_id: str, priority: AlarmPriority
    ) -> None:
        if not self.media_player_enabled or not self._media_call:
            return
        try:
            await self._media_call(rule_id, priority)
        except Exception:  # pragma: no cover - defensive around HA service calls
            _LOGGER.exception("Failed to play alarm sound through media players")

    def _sound_cooldown_elapsed(self) -> bool:
        if self.last_sound_at is None or self.repeat_interval_seconds <= 0:
            return True
        return self._now() - self.last_sound_at >= timedelta(
            seconds=self.repeat_interval_seconds
        )

    def as_dict(self) -> dict[str, Any]:
        """Return API status."""

        return {
            "test_sound_at": self.test_sound_at.isoformat() if self.test_sound_at else None,
            "sound_mode": self.sound_mode,
            "repeat_until_silenced": self.repeat_until_silenced,
            "repeat_interval_seconds": self.repeat_interval_seconds,
            "browser_enabled": self.browser_enabled,
            "media_player_enabled": self.media_player_enabled,
            "media_players": self.media_players,
            "horn_active": self.horn_active,
            "silenced": self.silenced,
            "silenced_until": self.silenced_until.isoformat()
            if self.silenced_until
            else None,
            "active_audible_alarms": list(self.active_audible_alarms),
            "last_sound_at": self.last_sound_at.isoformat()
            if self.last_sound_at
            else None,
        }
