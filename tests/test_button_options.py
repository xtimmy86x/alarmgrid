"""Exercise optional rule buttons with the real platform and a small HA fixture."""

import importlib.util
import sys
import unittest
from contextlib import contextmanager
from pathlib import Path
from types import ModuleType, SimpleNamespace
from unittest.mock import AsyncMock, patch

from custom_components.alarmgrid import AlarmGridRuntime
from custom_components.alarmgrid.alarm_engine import AlarmEngine
from custom_components.alarmgrid.alarm_models import AlarmLifecycleState, AlarmRule
from custom_components.alarmgrid.const import CONF_CREATE_RULE_BUTTONS, DEFAULT_OPTIONS, DOMAIN
from custom_components.alarmgrid.rule_management import per_rule_button_unique_ids


@contextmanager
def button_platform(registry, platform_name="button"):
    """Load actual entity classes without requiring a full HA installation."""
    modules = {name: ModuleType(name) for name in (
        "homeassistant", "homeassistant.components", "homeassistant.components.button",
        "homeassistant.components.switch",
        "homeassistant.config_entries", "homeassistant.core", "homeassistant.helpers",
        "homeassistant.helpers.entity", "homeassistant.helpers.entity_platform",
        "homeassistant.helpers.entity_registry",
    )}
    modules["homeassistant.components.button"].ButtonEntity = type("ButtonEntity", (), {})
    modules["homeassistant.components.button"].ButtonEntityDescription = SimpleNamespace
    modules["homeassistant.components.switch"].SwitchEntity = type("SwitchEntity", (), {})
    modules["homeassistant.components.switch"].SwitchEntityDescription = SimpleNamespace
    modules["homeassistant.config_entries"].ConfigEntry = object
    modules["homeassistant.core"].HomeAssistant = object
    modules["homeassistant.helpers.entity"].Entity = type("Entity", (), {})
    modules["homeassistant.helpers.entity"].DeviceInfo = dict
    modules["homeassistant.helpers.entity_platform"].AddEntitiesCallback = object
    modules["homeassistant.helpers.entity_registry"].async_get = lambda hass: registry
    modules["homeassistant.helpers.entity_registry"].async_entries_for_config_entry = (
        lambda reg, entry_id: [entry for entry in reg.entities.values() if entry.config_entry_id == entry_id]
    )
    root = Path(__file__).resolve().parents[1] / "custom_components/alarmgrid"
    with patch.dict(sys.modules, modules):
        for filename in ("entity_base", platform_name):
            name = f"custom_components.alarmgrid.{filename}"
            spec = importlib.util.spec_from_file_location(name, root / f"{filename}.py")
            module = importlib.util.module_from_spec(spec)
            sys.modules[name] = module
            spec.loader.exec_module(module)
        yield module


class ButtonOptionsTests(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.rule = AlarmRule.from_dict({
            "id": "alarm", "name": "Alarm", "entity_id": "binary_sensor.source", "condition": "is_on",
        })
        self.runtime = AlarmGridRuntime(
            entry_id="entry", rule_store=None, history_store=None,
            sound_manager=SimpleNamespace(test_sound=AsyncMock()),
            notification_manager=None, engine=AlarmEngine([self.rule]),
        )
        self.entry = SimpleNamespace(entry_id="entry")
        self.hass = SimpleNamespace(data={DOMAIN: {"entry": self.runtime}})
        self.registry = SimpleNamespace(entities={})
        self.registry.async_remove = lambda entity_id: self.registry.entities.pop(entity_id)

    async def setup_buttons(self):
        entities = []
        with button_platform(self.registry) as platform:
            await platform.async_setup_entry(self.hass, self.entry, entities.extend)
        for entity in entities:
            entity.hass = self.hass
            entity._context = SimpleNamespace(user_id=None)
        return entities

    def add_registry_entry(self, entity_id, unique_id, config_entry_id="entry"):
        self.registry.entities[entity_id] = SimpleNamespace(
            entity_id=entity_id, unique_id=unique_id, config_entry_id=config_entry_id,
        )

    async def test_default_preserves_global_and_per_rule_buttons_and_actions(self):
        self.assertTrue(DEFAULT_OPTIONS[CONF_CREATE_RULE_BUTTONS])
        self.assertTrue(self.runtime.create_rule_buttons)
        entities = await self.setup_buttons()
        self.assertEqual(len(entities), 7)
        buttons = {entity.entity_description.key: entity for entity in entities}
        self.assertEqual(set(buttons), {
            "acknowledge_all", "silence_horn", "unsilence_horn", "test_sound",
            "ack_alarm", "shelve_alarm", "disable_alarm",
        })
        self.runtime.engine.states["alarm"].lifecycle_state = AlarmLifecycleState.ACTIVE_UNACK
        await buttons["ack_alarm"].async_press()
        self.assertEqual(self.runtime.engine.states["alarm"].lifecycle_state, AlarmLifecycleState.ACTIVE_ACK)

    async def test_turning_off_removes_only_matching_per_rule_button_entries(self):
        self.runtime.create_rule_buttons = False
        for index, unique_id in enumerate(per_rule_button_unique_ids("entry", self.rule)):
            # Cleanup uses unique IDs, even when users have renamed entity IDs.
            self.add_registry_entry(f"button.renamed_{index}", unique_id)
        untouched = {
            "binary_sensor.alarm": "alarmgrid_entry_alarm_alarm",
            "button.acknowledge_all": "alarmgrid_entry_acknowledge_all",
            "button.silence_horn": "alarmgrid_entry_silence_horn",
            "button.unrelated": "unrelated_unique_id",
            "sensor.same_unique_id": "alarmgrid_entry_ack_alarm_alarm",
        }
        for entity_id, unique_id in untouched.items():
            self.add_registry_entry(entity_id, unique_id)
        self.add_registry_entry("button.other_entry", "alarmgrid_entry_ack_alarm_alarm", "other")
        entities = await self.setup_buttons()
        self.assertEqual(len(entities), 4)
        self.assertTrue(all(not hasattr(entity, "rule_id") for entity in entities))
        self.assertEqual(set(self.registry.entities), {*untouched, "button.other_entry"})
        self.assertIn("alarm", self.runtime.engine.rules)

        self.runtime.engine.states["alarm"].lifecycle_state = AlarmLifecycleState.ACTIVE_UNACK
        ack_all = next(entity for entity in entities if entity.entity_description.key == "acknowledge_all")
        await ack_all.async_press()
        self.assertEqual(self.runtime.engine.states["alarm"].lifecycle_state, AlarmLifecycleState.ACTIVE_ACK)

    async def test_new_rules_stay_without_buttons_until_option_is_reenabled(self):
        self.runtime.create_rule_buttons = False
        self.assertEqual(len(await self.setup_buttons()), 4)
        await self.runtime.engine.create_rule({
            "id": "second", "name": "Second", "entity_id": "binary_sensor.second", "condition": "is_on",
        })
        self.assertEqual(len(await self.setup_buttons()), 4)
        self.runtime.create_rule_buttons = True
        entities = await self.setup_buttons()
        self.assertEqual(len(entities), 10)
        actual = {entity._attr_unique_id for entity in entities if hasattr(entity, "rule_id")}
        expected = set().union(*(per_rule_button_unique_ids("entry", rule) for rule in self.runtime.engine.rules.values()))
        self.assertEqual(actual, expected)
        self.assertEqual(len(await self.setup_buttons()), 10)


    async def test_button_actions_snapshot_user_context(self):
        from custom_components.alarmgrid.alarm_notifications import TelegramNotifier
        from tests.test_notifications import options

        send = AsyncMock()
        notifier = TelegramNotifier(options(telegram_min_priority="status"), send)
        self.runtime.engine._event_handler = notifier.notify
        user = SimpleNamespace(id="user-id", name="Mario Rossi")
        self.hass.auth = SimpleNamespace(async_get_user=AsyncMock(return_value=user))
        buttons = {e.entity_description.key: e for e in await self.setup_buttons()}
        await self.runtime.engine.process_state("binary_sensor.source", "on")
        send.reset_mock()
        for name in ("acknowledge_all", "silence_horn", "unsilence_horn", "shelve_alarm", "disable_alarm"):
            button = buttons[name]
            button._context = SimpleNamespace(user_id=user.id)
            await button.async_press()
            self.assertEqual(self.runtime.engine.history_store.events[-1].operator, "Mario Rossi (Home Assistant)")
        self.assertEqual(send.await_count, 2)
        self.assertTrue(all("Mario Rossi (Home Assistant)" in call.args[1] for call in send.await_args_list))
        # A subsequent automated call must not inherit the previous human actor.
        buttons["disable_alarm"]._context = SimpleNamespace(user_id=None)
        await buttons["disable_alarm"].async_press()
        self.assertEqual(self.runtime.engine.history_store.events[-1].operator, "Home Assistant (system/automation)")

    async def test_sound_switch_uses_action_context(self):
        self.runtime.sound_manager.sound_mode = "browser_only"
        self.hass.auth = SimpleNamespace(async_get_user=AsyncMock(return_value=SimpleNamespace(id="user-id", name="Maria")))
        with button_platform(self.registry, "switch") as platform:
            switch = platform.SoundEnabledSwitch(self.runtime)
        switch.hass = self.hass
        switch._context = SimpleNamespace(user_id="user-id")
        await switch.async_turn_off()
        await switch.async_turn_on()
        self.assertEqual([event.operator for event in self.runtime.engine.history_store.events], ["Maria (Home Assistant)"] * 2)
