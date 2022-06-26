from unittest.mock import MagicMock

from functions.hello.main import hello


def test_hello():
    body = {"name": "Hello, World!"}

    request_mock = MagicMock()
    request_mock.get_json.return_value = body

    result = hello(request_mock)

    assert (f"Hello <@{body['name']}>!", 200) == result


def test_hello_empty_name():
    body = {"name": ""}

    request_mock = MagicMock()
    request_mock.get_json.return_value = body

    result = hello(request_mock)

    assert ("Hello !", 200) == result


def test_hello_missing_name():
    body = {}

    request_mock = MagicMock()
    request_mock.get_json.return_value = body

    result = hello(request_mock)

    assert ("Hello !", 200) == result
