"""User-facing message regressions, exercising real engine event snapshots."""

import unittest
from dataclasses import replace
from datetime import UTC, datetime

from custom_components.alarmgrid.alarm_engine import AlarmEngine
from custom_components.alarmgrid.alarm_models import AlarmCondition, AlarmRule
from custom_components.alarmgrid.alarm_notifications import format_telegram_message
from tests.test_notifications import event


class TelegramMessageTests(unittest.IsolatedAsyncioTestCase):
    def engine(self, **changes):
        rule = AlarmRule.from_dict(
            {
                "id": "pressure",
                "name": "Pressione compressori bassa",
                "entity_id": "sensor.pressure",
                "condition": "below",
                "threshold": 7.5,
                "area": "Locale compressori",
                "priority": "medium",
                **changes,
            }
        )
        return AlarmEngine([rule], now=lambda: datetime(2026, 10, 29, 4, tzinfo=UTC))

    async def test_pressure_alarm_has_one_reading_and_localized_condition(self):
        engine = self.engine()
        await engine.process_state("sensor.pressure", "7.20")
        recorded = engine.history_store.events[0]
        message = format_telegram_message(recorded, "it")
        self.assertTrue(
            message.startswith("🟡 ALLARME ATTIVO\nPressione compressori bassa\n\n")
        )
        self.assertIn("Area: Locale compressori\nPriorità: MEDIA\n\n", message)
        self.assertIn("Valore: 7,2\nCondizione: inferiore a 7,5", message)
        self.assertNotIn("Stato:", message)
        self.assertNotIn("Motivo:", message)
        self.assertNotIn("below", message)
        self.assertEqual(message.count("Pressione compressori bassa"), 1)
        self.assertIn("\n\n🕒 29/10/2026", message)
        # Presentation must not rewrite the recorded event or its raw reading.
        self.assertEqual(recorded.source_state, "7.20")
        self.assertEqual(recorded.source_value, 7.2)
        self.assertEqual(recorded.message, "Pressione compressori bassa below 7.5")

    async def test_condition_snapshot_survives_later_rule_edits(self):
        engine = self.engine()
        await engine.process_state("sensor.pressure", "7.2")
        recorded = engine.history_store.events[0]
        await engine.update_rule("pressure", {"threshold": 9})
        message = format_telegram_message(recorded, "en")
        self.assertIn("Value: 7.2\nCondition: below 7.5", message)
        self.assertNotIn("Condition: below 9", message)

    async def test_cleared_reading_does_not_claim_activation_condition_is_true(self):
        engine = self.engine()
        await engine.process_state("sensor.pressure", "7.2")
        await engine.process_state("sensor.pressure", "8")
        message = format_telegram_message(engine.history_store.events[-1], "it")
        self.assertTrue(message.startswith("✅ RIENTRATO\n"))
        self.assertIn("Valore: 8", message)
        self.assertNotIn("Condizione:", message)
        self.assertNotIn("Stato:", message)

    async def test_rule_description_and_operator_comment_are_preserved(self):
        engine = self.engine(description="Controllare il compressore <A> & il filtro.")
        await engine.process_state("sensor.pressure", "7.2")
        message = format_telegram_message(engine.history_store.events[-1], "it")
        self.assertIn("Motivo: Controllare il compressore <A> & il filtro.", message)
        await engine.acknowledge_alarm(
            "pressure", operator="Mario Rossi (Telegram)", comment="Controllo avviato"
        )
        message = format_telegram_message(engine.history_store.events[-1], "it")
        self.assertIn(
            "Operatore: Mario Rossi (Telegram)\nMotivo: Controllo avviato", message
        )

    async def test_manual_message_is_never_treated_as_generated_rule_text(self):
        engine = self.engine()
        await engine.manual_alarm(
            "pressure",
            message="Pressione compressori bassa below 7.5",
            operator="Mario",
        )
        message = format_telegram_message(engine.history_store.events[-1], "it")
        self.assertIn("Stato: Manuale", message)
        self.assertIn("Motivo: Pressione compressori bassa below 7.5", message)
        self.assertNotIn("Condizione:", message)

    async def test_text_thresholds_remain_literal_while_labels_are_translated(self):
        cases = [
            ("equal", "FAULT_7.5", "FAULT_7.5", "uguale a “FAULT_7.5”"),
            ("not_equal", "ready", "fault", "diverso da “ready”"),
            ("contains", "<fault>", "Pump <fault>", "contiene “<fault>”"),
            ("above", 7.5, "8", "superiore a 7,5"),
        ]
        for condition, threshold, reading, expected in cases:
            with self.subTest(condition=condition):
                engine = self.engine()
                engine.rules["pressure"] = replace(
                    engine.rules["pressure"],
                    condition=AlarmCondition(condition),
                    threshold=threshold,
                )
                await engine.process_state("sensor.pressure", reading)
                message = format_telegram_message(engine.history_store.events[-1], "it")
                self.assertIn(f"Condizione: {expected}", message)

    async def test_expression_summary_is_localized_without_duplicate_state_or_reason(
        self,
    ):
        engine = self.engine(
            condition_expression={
                "type": "group",
                "operator": "and",
                "conditions": [
                    {
                        "type": "condition",
                        "entity_id": "sensor.pressure",
                        "operator": "below",
                        "value": 7.5,
                    },
                    {
                        "type": "condition",
                        "entity_id": "binary_sensor.enabled",
                        "operator": "is_on",
                    },
                ],
            }
        )
        await engine.reconcile_states(
            {"sensor.pressure": "7.2", "binary_sensor.enabled": "on"}
        )
        recorded = engine.history_store.events[-1]
        self.assertIn(
            "Condizioni: 2 su 2 soddisfatte", format_telegram_message(recorded, "it")
        )
        self.assertIn(
            "Conditions: 2 of 2 matched", format_telegram_message(recorded, "en")
        )
        self.assertNotIn("conditions matched", format_telegram_message(recorded, "it"))

    async def test_zero_and_distinct_state_are_not_lost_in_deduplication(self):
        message = format_telegram_message(
            event(source_state="0.00", source_value=0.0), "it"
        )
        self.assertIn("Valore: 0", message)
        self.assertNotIn("Stato:", message)
        message = format_telegram_message(
            event(source_state="unavailable", source_value=0), "it"
        )
        self.assertIn("Stato: Non disponibile\nValore: 0", message)

    async def test_long_payload_remains_bounded_with_operator_and_timestamp(self):
        recorded = event(
            tag="😀" * 5000,
            area="a" * 5000,
            system="s" * 5000,
            source_state="raw" * 5000,
            source_value="value" * 5000,
            operator="Mario",
            message="note " * 5000,
        )
        message = format_telegram_message(recorded, "it")
        self.assertLessEqual(len(message.encode("utf-16-le")) // 2, 4096)
        self.assertIn("Operatore: Mario", message)
        self.assertIn("\n\n🕒 29/08/2026", message)


if __name__ == "__main__":
    unittest.main()
