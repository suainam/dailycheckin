import json
import os
import stat
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from scripts.materialize_config import load_config, write_config


class ConfigMaterializationTests(unittest.TestCase):
    def test_load_config_requires_json_object(self):
        with self.assertRaisesRegex(ValueError, "JSON object"):
            load_config("[]")

    def test_write_config_uses_private_permissions(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "config.json"
            write_config({"BILIBILI": [{"cookie": "secret"}]}, path)

            self.assertEqual(json.loads(path.read_text(encoding="utf-8"))["BILIBILI"][0]["cookie"], "secret")
            self.assertEqual(stat.S_IMODE(path.stat().st_mode), 0o600)


class WorkflowContractTests(unittest.TestCase):
    def test_daily_workflow_has_bounded_read_only_execution(self):
        workflow = (Path(__file__).parents[1] / ".github/workflows/daily-checkin.yml").read_text(encoding="utf-8")

        self.assertIn("contents: read", workflow)
        self.assertIn("timeout-minutes: 20", workflow)
        self.assertIn("cancel-in-progress: false", workflow)
        self.assertIn("DAILYCHECKIN_CONFIG_JSON", workflow)
        self.assertIn("--fail-on-error", workflow)
        self.assertIn('cron: "01 00,17 * * *"', workflow)
        self.assertIn('timezone: "Asia/Shanghai"', workflow)
        self.assertNotIn("pull_request_target", workflow)


if __name__ == "__main__":
    unittest.main()
