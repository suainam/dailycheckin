import unittest
from argparse import Namespace
from unittest.mock import Mock, patch

from dailycheckin import main


class StrictExitTests(unittest.TestCase):
    def test_fail_on_error_exits_nonzero_after_all_accounts_run(self):
        failing = Mock()
        failing.main.side_effect = RuntimeError("failed")
        succeeding = Mock()
        succeeding.main.return_value = "ok"
        factory = Mock(side_effect=[failing, succeeding])

        with (
            patch.object(main, "parse_arguments", return_value=Namespace(include=None, exclude=None, fail_on_error=True)),
            patch.object(main, "checkin_map", {"TEST": ("Test", factory)}),
            patch.object(main, "check_config", return_value=({}, {"test": [{"id": 1}, {"id": 2}]})),
            patch.object(main, "push_message"),
            patch.object(main.requests, "get", side_effect=RuntimeError("offline")),
        ):
            with self.assertRaisesRegex(SystemExit, "1"):
                main.checkin()

        self.assertEqual(factory.call_count, 2)

    def test_default_mode_preserves_zero_exit_behavior(self):
        failing = Mock()
        failing.main.side_effect = RuntimeError("failed")

        with (
            patch.object(main, "parse_arguments", return_value=Namespace(include=None, exclude=None, fail_on_error=False)),
            patch.object(main, "checkin_map", {"TEST": ("Test", Mock(return_value=failing))}),
            patch.object(main, "check_config", return_value=({}, {"test": [{"id": 1}]})),
            patch.object(main, "push_message"),
            patch.object(main.requests, "get", side_effect=RuntimeError("offline")),
        ):
            self.assertIsNone(main.checkin())


if __name__ == "__main__":
    unittest.main()
