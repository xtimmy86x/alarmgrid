"""Delivery recovery tests with a durable-store double and deterministic clock."""

import asyncio
import copy
import unittest
from datetime import timedelta
from unittest.mock import patch

from custom_components.alarmgrid.notification_queue import (
    MAX_AGE_SECONDS,
    MAX_PENDING,
    NotificationDelivery,
    TelegramOutbox,
)


class Store:
    def __init__(self):
        self.data = None
        self.fail = False

    async def async_load(self):
        return copy.deepcopy(self.data)

    async def async_save(self, data):
        if self.fail:
            raise OSError("disk full")
        self.data = copy.deepcopy(data)


class OutboxTests(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.now = 1000.0
        self.store = Store()
        self.calls = []

    async def send(self, item):
        self.calls.append(item.id)

    def queue(self, send=None, skip=None):
        return TelegramOutbox(
            self.store,
            send or self.send,
            skip or (lambda _: None),
            now=lambda: self.now,
        )

    def item(self, identifier="a", target="notify.test", event="activated"):
        return NotificationDelivery(
            identifier,
            "rule_1",
            event,
            "high",
            "inherit",
            target,
            "Secret alarm text",
            False,
            self.now,
        )

    async def test_enqueue_is_durable_before_any_network_call(self):
        queue = self.queue()
        await queue.async_enqueue([self.item()])
        self.assertEqual(self.calls, [])
        self.assertEqual(self.store.data["pending"][0]["id"], "a")
        self.assertTrue(await queue.async_process_once())
        self.assertEqual(self.calls, ["a"])
        self.assertEqual(self.store.data["pending"], [])

    async def test_transient_failure_recovers_after_restart(self):
        async def offline(item):
            raise TimeoutError("https://api.telegram.org/botSECRET/sendMessage")

        queue = self.queue(offline)
        await queue.async_enqueue([self.item()])
        with self.assertLogs(
            "custom_components.alarmgrid.notification_queue", level="WARNING"
        ) as logs:
            await queue.async_process_once()
        self.assertIn("rule=rule_1", logs.output[0])
        self.assertIn("target=notify.test", logs.output[0])
        self.assertIn("retry_in=5.0s", logs.output[0])
        self.assertNotIn("SECRET", str(logs.output))
        await queue.async_close()
        restored = self.queue()
        await restored.async_load()
        self.assertFalse(await restored.async_process_once())
        self.now += 5
        await restored.async_process_once()
        self.assertEqual(self.calls, ["a"])
        self.assertEqual(restored.diagnostics()["pending"], 0)
        self.assertEqual(restored.diagnostics()["sent"], 1)

    async def test_failed_recipient_does_not_duplicate_successful_recipient(self):
        async def selective(item):
            self.calls.append(item.id)
            if item.target == "notify.bad":
                raise ConnectionError()

        queue = self.queue(selective)
        await queue.async_enqueue(
            [self.item("a", "notify.bad"), self.item("b", "notify.good")]
        )
        await queue.async_process_once()
        self.now += 0.1
        await queue.async_process_once()
        self.now += 5
        await queue.async_process_once()
        self.assertEqual(self.calls, ["a", "b", "a"])

    async def test_recipient_fifo_waits_for_activation_before_clear(self):
        queue = self.queue()
        first = self.item()
        first.next_attempt_at = self.now + 30
        await queue.async_enqueue([first, self.item("b", event="cleared")])
        self.assertFalse(await queue.async_process_once())
        self.now += 30
        await queue.async_process_once()
        self.assertFalse(await queue.async_process_once())
        self.now += 3.1
        await queue.async_process_once()
        self.assertEqual(self.calls, ["a", "b"])

    async def test_wrapped_retry_after_is_respected_across_recipients(self):
        class RetryAfter(Exception):
            retry_after = timedelta(seconds=60)

        async def limited(item):
            try:
                raise RetryAfter("secret")
            except RetryAfter as err:
                raise RuntimeError("wrapped secret") from err

        queue = self.queue(limited)
        await queue.async_enqueue([self.item(), self.item("b", "notify.other")])
        await queue.async_process_once()
        self.now += 59
        self.assertFalse(await queue.async_process_once())
        self.assertEqual(queue.diagnostics()["last_error"], "RetryAfter")
        restored = self.queue()
        await restored.async_load()
        self.assertFalse(await restored.async_process_once())
        self.now += 1
        self.assertTrue(await restored.async_process_once())
        self.assertEqual(self.calls, ["a"])

    async def test_recipient_rate_limit_survives_reload_after_success(self):
        queue = self.queue()
        await queue.async_enqueue([self.item(), self.item("b")])
        await queue.async_process_once()
        restored = self.queue()
        await restored.async_load()
        self.assertFalse(await restored.async_process_once())
        self.now += 3.1
        await restored.async_process_once()
        self.assertEqual(self.calls, ["a", "b"])

    async def test_permanent_failure_is_visible_without_retries_or_sensitive_logs(self):
        class Forbidden(Exception):
            pass

        async def forbidden(item):
            raise Forbidden("botSECRET Secret alarm text")

        queue = self.queue(forbidden)
        await queue.async_enqueue([self.item()])
        with self.assertLogs(
            "custom_components.alarmgrid.notification_queue", level="ERROR"
        ) as logs:
            await queue.async_process_once()
        self.assertIn("error=Forbidden", str(logs.output))
        self.assertNotIn("SECRET", str(logs.output))
        self.assertNotIn("Secret alarm text", str(logs.output))
        self.assertEqual(queue.diagnostics()["failed"], 1)
        self.assertEqual(queue.diagnostics()["pending"], 0)

    async def test_changed_preferences_cancel_restored_messages(self):
        queue = self.queue()
        await queue.async_enqueue([self.item()])
        restored = self.queue(skip=lambda _: "telegram_disabled")
        await restored.async_load()
        await restored.async_process_once()
        self.assertEqual(self.calls, [])
        self.assertEqual(restored.diagnostics()["skipped"], 1)

    async def test_expired_messages_and_queue_overflow_are_explicit_failures(self):
        queue = self.queue()
        await queue.async_enqueue([self.item(str(n)) for n in range(MAX_PENDING)])
        with self.assertLogs(
            "custom_components.alarmgrid.notification_queue", level="ERROR"
        ):
            await queue.async_enqueue([self.item("overflow")])
        self.assertEqual(queue.diagnostics()["pending"], MAX_PENDING)
        self.assertEqual(queue.diagnostics()["failed"], 1)
        self.now += MAX_AGE_SECONDS
        with self.assertLogs(
            "custom_components.alarmgrid.notification_queue", level="ERROR"
        ):
            await queue.async_process_once()
        self.assertEqual(queue.diagnostics()["expired"], 1)
        self.assertEqual(self.calls, [])

    async def test_storage_failure_keeps_memory_queue_and_can_recover(self):
        queue = self.queue()
        self.store.fail = True
        with self.assertLogs(
            "custom_components.alarmgrid.notification_queue", level="ERROR"
        ):
            await queue.async_enqueue([self.item()])
        self.assertTrue(queue.diagnostics()["storage_dirty"])
        self.assertEqual(queue.diagnostics()["pending"], 1)
        self.store.fail = False
        await queue.async_close()
        self.assertFalse(queue.diagnostics()["storage_dirty"])
        self.assertEqual(self.store.data["pending"][0]["id"], "a")

    async def test_background_worker_wakes_for_new_delivery_and_stops_cleanly(self):
        delivered = asyncio.Event()

        async def send(item):
            delivered.set()

        queue = self.queue(send)
        queue.start()
        await queue.async_enqueue([self.item()])
        await asyncio.wait_for(delivered.wait(), 1)
        await queue.async_close()
        self.assertEqual(queue.diagnostics()["sent"], 1)

    async def test_unload_keeps_inflight_delivery_for_reload(self):
        entered = asyncio.Event()

        async def blocked(item):
            entered.set()
            await asyncio.Event().wait()

        queue = self.queue(blocked)
        await queue.async_enqueue([self.item()])
        queue.start()
        await asyncio.wait_for(entered.wait(), 1)
        await queue.async_close()
        restored = self.queue()
        await restored.async_load()
        await restored.async_process_once()
        self.assertEqual(self.calls, ["a"])

    async def test_hung_service_times_out_and_is_retried(self):
        async def blocked(item):
            await asyncio.Event().wait()

        queue = self.queue(blocked)
        await queue.async_enqueue([self.item()])
        with patch(
            "custom_components.alarmgrid.notification_queue.SEND_TIMEOUT_SECONDS", 0.001
        ):
            await queue.async_process_once()
        self.assertEqual(queue.diagnostics()["last_error"], "TimeoutError")
        self.assertEqual(queue.diagnostics()["pending"], 1)

    async def test_diagnostics_do_not_expose_message_or_recipient(self):
        queue = self.queue()
        await queue.async_enqueue([self.item()])
        report = str(queue.diagnostics())
        self.assertNotIn("notify.test", report)
        self.assertNotIn("Secret alarm text", report)


if __name__ == "__main__":
    unittest.main()
