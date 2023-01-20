from unittest.mock import MagicMock

from functions.http.main import BASE_URL, DEFAULT_IMG, ERROR_URL, http


def test_http_with_empty_body():
    body = {}

    request_mock = MagicMock()
    request_mock.get_json.return_value = body

    result = http(request_mock)

    assert result == (ERROR_URL, 200)


def test_http_good_code():
    body = {"params": ["200"]}

    request_mock = MagicMock()
    request_mock.get_json.return_value = body

    result = http(request_mock)

    assert result == (BASE_URL + "200", 200)


def test_http_with_empty_params():
    body = {"params": []}

    request_mock = MagicMock()
    request_mock.get_json.return_value = body

    result = http(request_mock)

    assert result == (DEFAULT_IMG, 200)
