import unittest
from datetime import UTC, datetime, timedelta
from types import SimpleNamespace

from custom_components.alarmgrid.alarm_engine import AlarmEngine
from custom_components.alarmgrid.alarm_models import (
    AlarmLifecycleState,
    AlarmRule,
    AlarmRuntimeState,
)
from custom_components.alarmgrid.telegram_interactive import (
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
            self.assertEqual(parse_callback(f"ag:opaque:{action}"), ("opaque", action))

    def test_foreign_and_malformed_callbacks_are_ignored(self):
        for value in (
            None,
            "",
            "other:token:ack",
            "ag:token",
            "ag::ack",
            "ag:t:bad",
        ):
            self.assertIsNone(parse_callback(value))


class TelegramSessionTests(unittest.TestCase):
    def test_keyboard_uses_home_assistant_pair_format(self):
        subject, rule = manager()
        self.assertEqual(
            subject.keyboard("TOKEN", rule),
            [
                [
                    ["✅ Acknowledge", "ag:TOKEN:ack"],
                    ["💤 Suspend", "ag:TOKEN:shelve"],
                ],
                [["🚫 Disable", "ag:TOKEN:disable"]],
            ],
        )
        self.assertFalse(any(isinstance(button, dict) for row in subject.keyboard("TOKEN", rule) for button in row))

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
            {"id": "query", "data": "ag:missing:ack", "chat_id": 1}
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
                "data": "ag:token:ack",
                "chat_id": 11,
                "message": {"message_id": 21},
            }
        )
        self.assertEqual(
            subject.hass.services.calls[-1][2]["service_data"]["message"],
            "Action no longer available",
        )

    async def test_bot_is_bound_then_other_bot_is_rejected(self):
        subject, _ = manager()
        subject.add_session("token", "temperature", "notify.telegram", 10, 20, "alarm")
        await subject.handle_callback({"id": "one", "data": "ag:token:shelve", "chat_id": 10, "message": {"message_id": 20}, "bot": {"config_entry_id": "bot-one"}})
        self.assertEqual(subject.sessions["token"].config_entry_id, "bot-one")
        await subject.handle_callback({"id": "two", "data": "ag:token:ack", "chat_id": 10, "message": {"message_id": 20}, "bot": {"config_entry_id": "bot-two"}})
        data = subject.hass.services.calls[-1][2]["service_data"]
        self.assertEqual(data["message"], "Action no longer available")
        self.assertEqual(data["config_entry_id"], "bot-two")


class TelegramActionLifecycleTests(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.rule = AlarmRule.from_dict({"id": "alarm", "entity_id": "binary_sensor.alarm", "name": "Alarm", "condition": "is_on", "priority": "high"})
        self.engine = AlarmEngine([self.rule])
        self.engine.states["alarm"].lifecycle_state = AlarmLifecycleState.ACTIVE_UNACK
        self.services = FakeServices()
        hass = SimpleNamespace(config=SimpleNamespace(language="en"), services=self.services)
        self.subject = TelegramInteractiveManager(hass, self.engine, {})
        self.subject.add_session("token", "alarm", "notify.telegram", 10, 20, "alarm", "bot-one")

    async def callback(self, action):
        await self.subject.handle_callback({"id": f"query-{action}", "data": f"ag:token:{action}", "chat_id": 10, "message": {"message_id": 20}, "bot": {"config_entry_id": "bot-one"}})
        self.assertEqual(self.services.calls[-1][1], "answer_callback_query")

    async def test_ack_changes_real_engine_state_and_operator(self):
        await self.callback("ack")
        state = self.engine.states["alarm"]
        self.assertEqual(state.lifecycle_state, AlarmLifecycleState.ACTIVE_ACK)
        self.assertEqual(state.ack_user, "telegram")
        self.assertTrue(any(call[1] == "edit_replymarkup" for call in self.services.calls))

    async def test_shelve_submenu_and_duration_change_real_engine(self):
        await self.callback("shelve")
        submenu = self.services.calls[-2][2]["service_data"]["inline_keyboard"]
        self.assertEqual(submenu[0][1], ["1 hour", "ag:token:s60"])
        await self.callback("s60")
        state = self.engine.states["alarm"]
        self.assertEqual(state.lifecycle_state, AlarmLifecycleState.SHELVED)
        self.assertAlmostEqual((state.shelve_expiry - datetime.now(UTC)).total_seconds(), 3600, delta=5)

    async def test_disable_requires_confirmation_then_enable(self):
        await self.callback("disable")
        self.assertTrue(self.engine.rules["alarm"].enabled)
        await self.callback("disable_confirm")
        self.assertFalse(self.engine.rules["alarm"].enabled)
        self.assertEqual(self.engine.states["alarm"].lifecycle_state, AlarmLifecycleState.DISABLED)
        await self.callback("enable")
        self.assertTrue(self.engine.rules["alarm"].enabled)
        self.assertEqual(self.engine.states["alarm"].lifecycle_state, AlarmLifecycleState.NORMAL)

    async def test_unshelve_calls_real_engine(self):
        await self.callback("s60")
        await self.callback("unshelve")
        self.assertEqual(self.engine.states["alarm"].lifecycle_state, AlarmLifecycleState.NORMAL)

    async def test_shelve_rejected_after_alarm_clears_but_ack_remains_valid(self):
        self.engine.states["alarm"].lifecycle_state = AlarmLifecycleState.CLEARED_UNACK
        await self.callback("s60")
        self.assertEqual(self.engine.states["alarm"].lifecycle_state, AlarmLifecycleState.CLEARED_UNACK)
        self.assertEqual(self.services.calls[-1][2]["service_data"]["message"], "Action no longer available")
        await self.callback("ack")
        self.assertEqual(self.engine.states["alarm"].lifecycle_state, AlarmLifecycleState.CLEARED_ACK)

    async def test_cancel_restores_pair_keyboard_without_engine_action(self):
        await self.callback("cancel")
        answer = self.services.calls[-1][2]["service_data"]
        self.assertEqual(answer["message"], "Cancelled")
        markup = self.services.calls[-2][2]["service_data"]["inline_keyboard"]
        self.assertTrue(all(isinstance(button, list) for row in markup for button in row))
        self.assertEqual(self.engine.states["alarm"].lifecycle_state, AlarmLifecycleState.ACTIVE_UNACK)
