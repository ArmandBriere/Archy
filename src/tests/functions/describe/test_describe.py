from unittest.mock import MagicMock

import pytest

from functions.describe.main import describe


def test_describe():
    body = {"user_id": "123"}

    request_mock = MagicMock()
    request_mock.get_json.return_value = body

    result = describe(request_mock)

    assert (f"You are a big ****! <@{body['user_id']}>", 200) == result


def test_describe_empty_body():

    request_mock = MagicMock()
    request_mock.get_json.return_value = {}

    result = describe(request_mock)

    assert ("I don't even know who you are!", 200) == result


def test_hello_empty_user_id():
    body = {"user_id": ""}

    request_mock = MagicMock()
    request_mock.get_json.return_value = body

    result = describe(request_mock)

    assert ("I don't even know who you are!", 200) == result


@pytest.mark.parametrize(
    ("body"),
    [
        {
            "user_id": "123",
            "mentions": ["123"],
        },
        {
            "user_id": "123",
            "mentions": ["123", "456"],
        },
    ],
)
def test_describe_with_mentions(body):

    request_mock = MagicMock()
    request_mock.get_json.return_value = body

    result = describe(request_mock)

    assert (f"<@{body['mentions'][0]}> is a big ****!", 200) == result


def test_describe_protected_user():
    body = {"user_id": "123", "mentions": ["135048445097410560"]}

    request_mock = MagicMock()
    request_mock.get_json.return_value = body

    result = describe(request_mock)

    assert ("This person is awesome!", 200) == result
