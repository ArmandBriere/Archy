from unittest.mock import MagicMock

from functions.flag.main import flag


def test_flag():
    body = {}

    request_mock = MagicMock()
    request_mock.get_json.return_value = body

    result = flag(request_mock)

    the_flag = ":triangular_flag_on_post:"

    assert result == (the_flag, 200)
