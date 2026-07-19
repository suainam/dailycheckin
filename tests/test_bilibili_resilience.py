import unittest
from unittest.mock import Mock, patch

from dailycheckin.bilibili.main import BiliBili, safe_json


class BilibiliResilienceTests(unittest.TestCase):
    def test_safe_json_returns_fallback_for_invalid_response(self):
        response = Mock(status_code=502, text="upstream error")
        response.json.side_effect = ValueError("invalid json")
        fallback = {"code": -1, "data": {}}

        with patch("builtins.print") as output:
            self.assertIs(safe_json(response, fallback, "test"), fallback)

        self.assertNotIn("upstream error", str(output.call_args_list))

    def test_null_collections_become_empty(self):
        session = Mock()
        session.get.return_value.json.return_value = {"data": None}

        self.assertEqual(BiliBili.get_today_exp(session), [])
        self.assertEqual(BiliBili.reward(session), [])
        self.assertEqual(BiliBili.get_region(session), [])

    def test_main_skips_video_tasks_when_region_is_empty(self):
        checkin = BiliBili({"cookie": "SESSDATA=value; bili_jct=csrf", "coin_num": 0, "coin_type": 0})
        initial_nav = ("user", 1, True, 10, 0, 100)
        final_nav = ("user", 1, True, 10, 0, 100)

        with (
            patch("dailycheckin.bilibili.main.requests.session"),
            patch.object(checkin, "get_nav", side_effect=[initial_nav, final_nav]),
            patch.object(checkin, "manga_sign", return_value="ok"),
            patch.object(checkin, "live_sign", return_value="ok"),
            patch.object(checkin, "get_region", return_value=[]),
            patch.object(checkin, "vip_privilege_my", return_value={"data": {"list": []}}),
            patch.object(checkin, "get_today_exp", return_value=[]),
            patch.object(checkin, "live_status", return_value=[]),
            patch.object(checkin, "report_task") as report_task,
            patch.object(checkin, "share_task") as share_task,
        ):
            result = checkin.main()

        report_task.assert_not_called()
        share_task.assert_not_called()
        self.assertIn("无可用视频，跳过观看任务", result)
        self.assertIn("无可用视频，跳过分享任务", result)


if __name__ == "__main__":
    unittest.main()
