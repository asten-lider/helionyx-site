"""Regression tests for payment-state safety; no real providers or charges."""
import importlib.util
import os
import pathlib
import sqlite3
import tempfile
import unittest
from unittest.mock import patch

MODULE_PATH = pathlib.Path(__file__).resolve().parents[1] / "server" / "app.py"
spec = importlib.util.spec_from_file_location("helionyx_server", MODULE_PATH)
app = importlib.util.module_from_spec(spec)
spec.loader.exec_module(app)


class PaymentStateTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.previous_db_path = app.DB_PATH
        app.DB_PATH = os.path.join(self.tmp.name, "orders.sqlite3")
        with app.db_connect() as db:
            db.execute(
                """INSERT INTO orders
                   (id, created_at, updated_at, status, payment_id, amount,
                    customer_name, phone, email, details_json)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                ("HNX-20261020-TEST", "2026-10-20", "2026-10-20",
                 "paid", "test-payment", 3190, "Tester", "79990000000",
                 "test@example.org", "{}"),
            )
            db.commit()

    def tearDown(self):
        app.DB_PATH = self.previous_db_path
        self.tmp.cleanup()

    def status(self):
        return app.get_order("HNX-20261020-TEST")["status"]

    def test_fulfilled_cannot_revert_to_paid_or_pending(self):
        app.update_order("HNX-20261020-TEST", "fulfilled")
        for incoming in ("paid", "pending", "canceled", "payment_error"):
            app.update_order("HNX-20261020-TEST", incoming)
            self.assertEqual(self.status(), "fulfilled")

    def test_refund_cannot_revert_to_paid(self):
        for state in ("refunded", "partially_refunded"):
            app.update_order("HNX-20261020-TEST", state)
            for incoming in ("paid", "pending", "canceled"):
                app.update_order("HNX-20261020-TEST", incoming)
                self.assertEqual(self.status(), state)

    def test_payment_callback_does_not_ship_refunded_order(self):
        app.update_order("HNX-20261020-TEST", "refunded")
        payment = {
            "metadata": {"order_id": "HNX-20261020-TEST"},
            "amount": {"value": "3190.00"},
            "status": "succeeded",
            "paid": True,
        }
        with patch.object(app, "yookassa_request", return_value=payment), \
             patch.object(app, "create_cdek_shipment_safely") as ship:
            app.verify_payment("test-payment")
        self.assertEqual(self.status(), "refunded")
        ship.assert_not_called()

    def test_success_callback_keeps_paid_order_paid(self):
        payment = {
            "metadata": {"order_id": "HNX-20261020-TEST"},
            "amount": {"value": "3190.00"},
            "status": "succeeded",
            "paid": True,
        }
        with patch.object(app, "yookassa_request", return_value=payment), \
             patch.object(app, "create_cdek_shipment_safely") as ship:
            app.verify_payment("test-payment")
        self.assertEqual(self.status(), "paid")
        ship.assert_called_once()

    def test_spoofed_real_ip_only_trusted_from_loopback(self):
        class FakeHandler:
            def __init__(self, peer, claimed):
                self.client_address = (peer, 5555)
                self.headers = {"X-Real-IP": claimed}
        self.assertEqual(app.client_ip(FakeHandler("192.0.2.7", "1.2.3.4")), "192.0.2.7")
        self.assertEqual(app.client_ip(FakeHandler("127.0.0.1", "1.2.3.4")), "1.2.3.4")
        self.assertEqual(app.client_ip(FakeHandler("127.0.0.1", "invalid")), "127.0.0.1")


if __name__ == "__main__":
    unittest.main()
