import unittest
from unittest.mock import Mock, patch

from dailycheckin.tieba.main import Tieba


class TiebaSupplementTests(unittest.TestCase):
    def test_concurrency_defaults_to_one_and_is_capped_at_two(self):
        self.assertEqual(Tieba({"cookie": "BDUSS=test"}).concurrency, 1)
        self.assertEqual(Tieba({"cookie": "BDUSS=test", "concurrency": 9}).concurrency, 2)
        self.assertEqual(Tieba({"cookie": "BDUSS=test", "concurrency": "invalid"}).concurrency, 1)

    def test_sign_forums_skips_forums_already_signed(self):
        tieba = Tieba({"cookie": "BDUSS=test; STOKEN=test"})
        tieba.request = Mock(return_value={"error_code": "0"})
        forums = [
            {"id": "1", "name": "already", "is_sign": "1"},
            {"id": "2", "name": "pending", "is_sign": "0"},
        ]

        with patch("dailycheckin.tieba.main.time.sleep") as sleep:
            stats = tieba.sign_forums(forums, "test-tbs")

        self.assertEqual(stats, {"total": 2, "success": 1, "exist": 1, "shield": 0, "error": 0})
        self.assertEqual(tieba.request.call_count, 1)
        self.assertEqual(tieba.request.call_args.args[2]["fid"], "2")
        self.assertEqual(sleep.call_count, 1)

    def test_get_favorite_prefers_list_with_sign_status(self):
        tieba = Tieba({"cookie": "BDUSS=test"})
        tieba.request = Mock(
            return_value={
                "no": 0,
                "data": {
                    "like_forum": [
                        {"forum_id": 1, "forum_name": "already", "is_sign": 1},
                        {"forum_id": 2, "forum_name": "pending", "is_sign": 0},
                    ]
                },
            }
        )

        self.assertEqual(
            tieba.get_favorite(),
            [
                {"id": "1", "name": "already", "is_sign": 1},
                {"id": "2", "name": "pending", "is_sign": 0},
            ],
        )
        tieba.request.assert_called_once_with(tieba.STATUS_LIKE_URL)

    def test_sign_forums_treats_boolean_signed_state_as_signed(self):
        tieba = Tieba({"cookie": "BDUSS=test"})
        tieba.request = Mock(return_value={"error_code": "0"})

        with patch("dailycheckin.tieba.main.time.sleep"):
            stats = tieba.sign_forums([{"id": "1", "name": "already", "is_sign": True}], "test-tbs")

        self.assertEqual(stats["exist"], 1)
        tieba.request.assert_not_called()

    def test_get_user_info_prefers_tieba_display_name(self):
        tieba = Tieba({"cookie": "BDUSS=test"})
        tieba.request = Mock(
            side_effect=[
                {"is_login": 1, "tbs": "test-tbs"},
                {"data": {"user_name_show": "贴吧昵称"}},
            ]
        )

        self.assertEqual(tieba.get_user_info(), ("test-tbs", "贴吧昵称"))

    def test_get_user_info_falls_back_to_baidu_username(self):
        tieba = Tieba({"cookie": "BDUSS=test"})
        tieba.request = Mock(
            side_effect=[
                {"is_login": 1, "tbs": "test-tbs"},
                None,
                {"userName": "百度用户名"},
            ]
        )

        self.assertEqual(tieba.get_user_info(), ("test-tbs", "百度用户名"))

    def test_get_user_info_falls_back_when_tieba_profile_request_fails(self):
        tieba = Tieba({"cookie": "BDUSS=test"})
        tieba.request = Mock(
            side_effect=[
                {"is_login": 1, "tbs": "test-tbs"},
                Exception("profile unavailable"),
                {"userName": "百度用户名"},
            ]
        )

        self.assertEqual(tieba.get_user_info(), ("test-tbs", "百度用户名"))


if __name__ == "__main__":
    unittest.main()
