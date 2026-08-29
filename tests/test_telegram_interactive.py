import unittest
from datetime import UTC, datetime, timedelta
from types import SimpleNamespace

from custom_components.industrial_alarm_panel.alarm_models import (
    AlarmLifecycleState,
    AlarmRule,
    AlarmRuntimeState,
)
from custom_components.industrial_alarm_panel.telegram_interactive import (
    MAX_SESSIONS,
    SHELVE_MINUTES,
    TelegramInteractiveManager,
    parse_callback,
)


class FakeServices:
    def __init__(self):
        self.calls = []

    async def async_call(self, domain, service, **kwargs):
        self.calls.append((domain, service, kwargs))


def manager():
    rule = AlarmRule.from_dict(
        {
            "id": "temperature",
            "entity_id": "sensor.temperature",
            "name": "Temperature",
            "condition": "equal",
            "threshold": 1,
            "priority": "critical",
        }
    )
    engine = SimpleNamespace(
        rules={rule.id: rule},
        states={
            rule.id: AlarmRuntimeState(
                rule_id=rule.id,
                lifecycle_state=AlarmLifecycleState.ACTIVE_UNACK,
            )
        },
    )
    hass = SimpleNamespace(
        config=SimpleNamespace(language="en"), services=FakeServices()
    )
    return TelegramInteractiveManager(hass, engine, {}), rule


class TelegramCallbackParserTests(unittest.TestCase):
    def test_all_supported_callbacks(self):
        actions = {
            "ack",
            "shelve",
            "disable",
            "disable_confirm",
            "unshelve",
            "enable",
            "cancel",
            *SHELVE_MINUTES,
        }
        for action in actions:
            self.assertEqual(parse_callback(f"iap:opaque:{action}"), ("opaque", action))

    def test_foreign_and_malformed_callbacks_are_ignored(self):
        for value in (
            None,
            "",
            "other:token:ack",
            "iap:token",
            "iap::ack",
            "iap:t:bad",
        ):
            self.assertIsNone(parse_callback(value))


class TelegramSessionTests(unittest.TestCase):
    def test_tokens_are_unique_and_opaque(self):
        subject, _ = manager()
        tokens = {subject.new_token() for _ in range(100)}
        self.assertEqual(len(tokens), 100)
        self.assertTrue(all(len(token) >= 16 for token in tokens))

    def test_expired_sessions_are_removed(self):
        subject, _ = manager()
        subject.add_session("old", "temperature", "notify.telegram", 1, 2, "alarm")
        subject.sessions["old"].created_at = datetime.now(UTC) - timedelta(days=8)
        subject.cleanup()
        self.assertNotIn("old", subject.sessions)

    def test_session_count_is_bounded(self):
        subject, _ = manager()
        for index in range(MAX_SESSIONS + 5):
            subject.add_session(
                str(index), "temperature", "notify.telegram", 1, index, "alarm"
            )
        self.assertEqual(len(subject.sessions), MAX_SESSIONS)


class TelegramCallbackTests(unittest.IsolatedAsyncioTestCase):
    async def test_expired_callback_is_answered_without_traceback(self):
        subject, _ = manager()
        await subject.handle_callback(
            {"id": "query", "data": "iap:missing:ack", "chat_id": 1}
        )
        self.assertEqual(subject.hass.services.calls[-1][1], "answer_callback_query")
        self.assertEqual(
            subject.hass.services.calls[-1][2]["service_data"]["message"],
            "Action expired",
        )

    async def test_chat_and_message_mismatch_are_rejected(self):
        subject, _ = manager()
        subject.add_session("token", "temperature", "notify.telegram", 10, 20, "alarm")
        await subject.handle_callback(
            {
                "id": "query",
                "data": "iap:token:ack",
                "chat_id": 11,
                "message": {"message_id": 21},
            }
        )
        self.assertEqual(
            subject.hass.services.calls[-1][2]["service_data"]["message"],
            "Action no longer available",
        )
