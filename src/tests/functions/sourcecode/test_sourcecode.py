from unittest.mock import MagicMock

from functions.src.main import SOURCE_CODE_URL, sourcecode


def test_sourcecode():
    body = {}

    request_mock = MagicMock()
    request_mock.get_json.return_value = body

    result = sourcecode(request_mock)

    assert result == (SOURCE_CODE_URL, 200)
