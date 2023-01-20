from unittest.mock import MagicMock, patch

from functions.http.main import BASE_URL, DEFAULT_IMG, ERROR_URL, http

MODULE_PATH = "functions.http.main"


@patch(f"{MODULE_PATH}.requests")
def test_http_with_empty_body(http_request_mock):
    body = {}

    request_mock = MagicMock()
    request_mock.get_json.return_value = body

    result = http(request_mock)

    assert result == (ERROR_URL, 200)
    assert http_request_mock.get.call_count == 0


@patch(f"{MODULE_PATH}.requests")
def test_http_bad_code(http_request_mock):
    http_request_mock.get.return_value.status_code = 404

    body = {"params": ["jfdhs2sd287ydfsu"]}

    request_mock = MagicMock()
    request_mock.get_json.return_value = body

    result = http(request_mock)

    assert result == (ERROR_URL, 200)
    assert http_request_mock.get.call_count == 1


@patch(f"{MODULE_PATH}.requests")
def test_http_good_code(http_request_mock):
    http_request_mock.get.return_value.status_code = 200

    body = {"params": ["200"]}

    request_mock = MagicMock()
    request_mock.get_json.return_value = body

    result = http(request_mock)

    assert result == (f"{BASE_URL}200", 200)
    assert http_request_mock.get.call_count == 1


@patch(f"{MODULE_PATH}.requests")
def test_http_with_empty_params(http_request_mock):
    body = {"params": []}

    request_mock = MagicMock()
    request_mock.get_json.return_value = body

    result = http(request_mock)

    assert result == (DEFAULT_IMG, 200)
    assert http_request_mock.get.call_count == 0
