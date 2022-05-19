from unittest.mock import MagicMock

from functions.hello.main import hello

MODULE_PATH = "functions.hello.main"


def test_hello():
    body = {"name": "Hello, World!"}

    request_mock = MagicMock()
    request_mock.get_json.return_value = body

    result = hello(request_mock)

    assert f"Hello @<{body['name']}>!" == result


def test_hello_empty_name():
    body = {"name": ""}

    request_mock = MagicMock()
    request_mock.get_json.return_value = body

    result = hello(request_mock)

    assert "Hello !" == result


def test_hello_missing_name():
    body = {}

    request_mock = MagicMock()
    request_mock.get_json.return_value = body

    result = hello(request_mock)

    assert "Hello !" == result
