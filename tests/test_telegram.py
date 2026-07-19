import unittest
from unittest.mock import Mock, patch

from dailycheckin.utils.message import message2telegram


class TelegramTests(unittest.TestCase):
    @patch("dailycheckin.utils.message.requests.post")
    def test_telegram_checks_http_and_api_result(self, post):
        response = Mock(status_code=200, text='{"ok": false}')
        response.json.return_value = {"ok": False, "description": "rejected"}
        post.return_value = response

        with patch("builtins.print") as output:
            with self.assertRaisesRegex(ValueError, "Telegram API"):
                message2telegram("", "", "token", "user", "message")

        response.raise_for_status.assert_called_once_with()
        rendered_output = str(output.call_args_list)
        self.assertNotIn("message", rendered_output)
        self.assertNotIn('{"ok": false}', rendered_output)


if __name__ == "__main__":
    unittest.main()
