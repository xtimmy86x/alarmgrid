"""Interactive Telegram alarm actions using Home Assistant's native services."""

from __future__ import annotations

import logging
import secrets
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from typing import Any

from .alarm_models import AlarmLifecycleState
from .telegram_i18n import telegram_language, telegram_text

_LOGGER = logging.getLogger(__name__)
SESSION_TTL = timedelta(days=7)
MAX_SESSIONS = 1000
SHELVE_MINUTES = {
    "s15": 15,
    "s60": 60,
    "s240": 240,
    "s480": 480,
    "s1440": 1440,
    "s4320": 4320,
    "s10080": 10080,
}
VALID_ACTIONS = {
    "ack",
    "shelve",
    "disable",
    "disable_confirm",
    "unshelve",
    "enable",
    "cancel",
    *SHELVE_MINUTES,
}


@dataclass(slots=True)
class TelegramActionSession:
    """Runtime-only association between an opaque callback and an alarm."""

    token: str
    rule_id: str
    target_entity_id: str
    chat_id: int
    message_id: int
    original_message: str
    created_at: datetime
    config_entry_id: str | None = None


def parse_callback(value: Any) -> tuple[str, str] | None:
    """Parse only well-formed callbacks owned by this integration."""

    if not isinstance(value, str):
        return None
    parts = value.split(":")
    if (
        len(parts) != 3
        or parts[0] != "ag"
        or not parts[1]
        or parts[2] not in VALID_ACTIONS
    ):
        return None
    return parts[1], parts[2]


class TelegramInteractiveManager:
    """Own bounded sessions and execute validated actions through AlarmEngine."""

    def __init__(self, hass: Any, engine: Any, options: dict[str, Any]) -> None:
        self.hass = hass
        self.engine = engine
        self.options = options
        self.sessions: dict[str, TelegramActionSession] = {}
        self.language = telegram_language(hass)
        self.text = _TelegramText(self.language)

    def cleanup(self, now: datetime | None = None) -> None:
        """Opportunistically discard expired and oldest excess sessions."""

        now = now or datetime.now(UTC)
        for token, session in list(self.sessions.items()):
            if now - session.created_at >= SESSION_TTL:
                self.sessions.pop(token, None)
        excess = len(self.sessions) - MAX_SESSIONS
        if excess > 0:
            oldest = sorted(self.sessions.values(), key=lambda item: item.created_at)
            for session in oldest[:excess]:
                self.sessions.pop(session.token, None)

    def new_token(self) -> str:
        """Return a compact cryptographically unpredictable unique token."""

        self.cleanup()
        while (token := secrets.token_urlsafe(12)) in self.sessions:
            pass
        return token

    def keyboard(
        self, token: str, rule: Any | None = None
    ) -> list[list[list[str]]]:
        """Build the main keyboard from global and current rule capabilities."""

        if rule is None:
            return []
        buttons = []
        state = self.engine.states.get(rule.id)
        if (
            self.options.get("telegram_interactive_ack", True)
            and rule.requires_ack
            and state is not None
            and state.is_unacknowledged
        ):
            buttons.append(self._button(f"✅ {self.text['ack']}", token, "ack"))
        if (
            self.options.get("telegram_interactive_shelve", True)
            and rule.enabled
            and rule.shelving_allowed
            and state is not None
            and state.lifecycle_state in _ACTIVE_STATES
        ):
            buttons.append(self._button(f"💤 {self.text['shelve']}", token, "shelve"))
        rows = [buttons] if buttons else []
        if self.options.get("telegram_interactive_disable", True) and rule.enabled:
            rows.append([self._button(f"🚫 {self.text['disable']}", token, "disable")])
        return rows

    @staticmethod
    def _button(text: str, token: str, action: str) -> list[str]:
        """Build the two-item sequence parsed by Home Assistant telegram_bot."""
        return [text, f"ag:{token}:{action}"]

    def add_session(
        self,
        token: str,
        rule_id: str,
        target: str,
        chat_id: Any,
        message_id: Any,
        message: str,
        config_entry_id: str | None = None,
    ) -> TelegramActionSession:
        self.cleanup()
        session = TelegramActionSession(
            token,
            rule_id,
            target,
            int(chat_id),
            int(message_id),
            message,
            datetime.now(UTC),
            config_entry_id,
        )
        self.sessions[token] = session
        self.cleanup()
        return session

    async def handle_callback(self, attributes: dict[str, Any]) -> None:
        """Validate and process one telegram_callback event entity update."""

        parsed = parse_callback(attributes.get("data") or attributes.get("command"))
        if parsed is None:
            return
        token, action = parsed
        callback_id = attributes.get("id")
        bot = attributes.get("bot")
        callback_config_entry_id = (
            bot.get("config_entry_id") if isinstance(bot, dict) else None
        )
        self.cleanup()
        session = self.sessions.get(token)
        if session is None:
            await self._answer(callback_id, self.text["expired"], callback_config_entry_id)
            return
        if session.config_entry_id is None and callback_config_entry_id:
            session.config_entry_id = callback_config_entry_id
        elif (
            session.config_entry_id is not None
            and callback_config_entry_id != session.config_entry_id
        ):
            await self._answer(callback_id, self.text["unavailable"], callback_config_entry_id)
            return
        message = attributes.get("message") or {}
        callback_message_id = (
            message.get("message_id") if isinstance(message, dict) else None
        )
        try:
            chat_matches = int(attributes.get("chat_id")) == session.chat_id
            message_matches = (
                callback_message_id is None
                or int(callback_message_id) == session.message_id
            )
        except (TypeError, ValueError):
            chat_matches = message_matches = False
        rule = self.engine.rules.get(session.rule_id)
        if not chat_matches or not message_matches or rule is None:
            await self._answer(callback_id, self.text["unavailable"], session.config_entry_id)
            return
        try:
            answer = await self._execute(session, rule, action)
        except Exception:
            _LOGGER.warning("Interactive Telegram alarm action failed", exc_info=True)
            answer = self.text["unavailable"]
        await self._answer(callback_id, answer, session.config_entry_id)

    async def _execute(
        self, session: TelegramActionSession, rule: Any, action: str
    ) -> str:
        state = self.engine.states[session.rule_id]
        lifecycle = state.lifecycle_state
        if action == "cancel":
            await self._markup(session, self.keyboard(session.token, rule))
            return self.text["cancelled"]
        if action == "shelve":
            if (
                not self.options.get("telegram_interactive_shelve", True)
                or not rule.enabled
                or not rule.shelving_allowed
                or lifecycle not in _ACTIVE_STATES
            ):
                return self.text["unavailable"]
            durations = [
                (self.text[f"duration_{minutes}"], code)
                for code, minutes in SHELVE_MINUTES.items()
            ]
            rows = [
                [
                    self._button(label, session.token, code)
                    for label, code in durations[:3]
                ],
                [
                    self._button(label, session.token, code)
                    for label, code in durations[3:6]
                ],
                [self._button(durations[6][0], session.token, durations[6][1])],
                [self._button(f"← {self.text['cancel']}", session.token, "cancel")],
            ]
            await self._markup(session, rows)
            return self.text["choose"]
        if action == "disable":
            if (
                not self.options.get("telegram_interactive_disable", True)
                or not rule.enabled
            ):
                return self.text["unavailable"]
            await self._markup(
                session,
                [
                    [
                        self._button(
                            f"⚠️ {self.text['confirm']}",
                            session.token,
                            "disable_confirm",
                        ),
                        self._button(
                            f"← {self.text['cancel']}", session.token, "cancel"
                        ),
                    ]
                ],
            )
            return self.text["disable_q"]
        if action == "ack":
            if (
                not self.options.get("telegram_interactive_ack", True)
                or not state.is_unacknowledged
                or not rule.requires_ack
            ):
                return self.text["unavailable"]
            await self.engine.acknowledge_alarm(session.rule_id, operator="telegram")
            await self._markup(session, self.keyboard(session.token, rule))
            return self.text["ack_ok"]
        if action in SHELVE_MINUTES:
            if (
                not self.options.get("telegram_interactive_shelve", True)
                or not rule.enabled
                or not rule.shelving_allowed
                or lifecycle not in _ACTIVE_STATES
            ):
                return self.text["unavailable"]
            await self.engine.shelve_alarm(
                session.rule_id,
                duration_minutes=SHELVE_MINUTES[action],
                operator="telegram",
                comment="Shelved from Telegram",
            )
            until = self.engine.states[session.rule_id].shelve_expiry
            await self._edit(
                session,
                f"{session.original_message}\n\n💤 "
                + self.text["shelve_until"].format(
                    time=until.astimezone().strftime("%H:%M")
                ),
                [
                    [
                        self._button(
                            f"🔔 {self.text['unshelve']}", session.token, "unshelve"
                        )
                    ]
                ],
            )
            return self.text["shelve_ok"]
        if action == "unshelve" and lifecycle == AlarmLifecycleState.SHELVED:
            await self.engine.unshelve_alarm(session.rule_id, operator="telegram")
            await self._edit(
                session,
                f"{session.original_message}\n\n🔔 {self.text['unshelve_ok']}",
                [],
            )
            return self.text["unshelve_ok"]
        if (
            action == "disable_confirm"
            and self.options.get("telegram_interactive_disable", True)
            and rule.enabled
        ):
            await self.engine.disable_alarm(
                session.rule_id, operator="telegram", comment="Disabled from Telegram"
            )
            await self._edit(
                session,
                f"{session.original_message}\n\n🚫 {self.text['disable_ok']}",
                [[self._button(f"▶️ {self.text['enable']}", session.token, "enable")]],
            )
            return self.text["disable_ok"]
        if action == "enable" and not rule.enabled:
            await self.engine.enable_alarm(session.rule_id, operator="telegram")
            await self._edit(
                session, f"{session.original_message}\n\n▶️ {self.text['enable_ok']}", []
            )
            return self.text["enable_ok"]
        return self.text["unavailable"]

    async def _call(
        self, service: str, data: dict[str, Any], config_entry_id: str | None = None
    ) -> Any:
        if config_entry_id:
            data = {**data, "config_entry_id": config_entry_id}
        return await self.hass.services.async_call(
            "telegram_bot", service, service_data=data, blocking=True
        )

    async def _answer(
        self, callback_id: Any, message: str, config_entry_id: str | None = None
    ) -> None:
        if not callback_id:
            return
        try:
            await self._call(
                "answer_callback_query",
                {"callback_query_id": callback_id, "message": message},
                config_entry_id,
            )
        except Exception:
            _LOGGER.warning("Could not answer Telegram callback", exc_info=True)

    async def _markup(
        self, session: TelegramActionSession, keyboard: list[Any]
    ) -> None:
        try:
            await self._call(
                "edit_replymarkup",
                {
                    "chat_id": session.chat_id,
                    "message_id": session.message_id,
                    "inline_keyboard": keyboard,
                },
                session.config_entry_id,
            )
        except Exception:
            _LOGGER.warning("Could not update Telegram reply markup", exc_info=True)

    async def _edit(
        self, session: TelegramActionSession, message: str, keyboard: list[Any]
    ) -> None:
        try:
            await self._call(
                "edit_message",
                {
                    "chat_id": session.chat_id,
                    "message_id": session.message_id,
                    "message": message,
                    "inline_keyboard": keyboard,
                },
                session.config_entry_id,
            )
        except Exception:
            _LOGGER.warning("Could not edit Telegram message", exc_info=True)


_ACTIVE_STATES = {
    AlarmLifecycleState.ACTIVE_UNACK,
    AlarmLifecycleState.ACTIVE_ACK,
}


class _TelegramText:
    """Mapping-like compatibility wrapper around the shared translator."""

    def __init__(self, language: str) -> None:
        self.language = language

    def __getitem__(self, key: str) -> str:
        return telegram_text(self.language, key)
