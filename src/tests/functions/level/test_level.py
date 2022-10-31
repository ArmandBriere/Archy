# pylint: disable=line-too-long

import json
from unittest.mock import MagicMock, patch

from functions.level.main import level, publish_generate_image

MODULE_PATH = "functions.level.main"


def get_db_value(param):  # pragma: no cover
    if param == "level":
        return 1
    if param == "rank":
        return 1

    return 0


@patch(f"{MODULE_PATH}.publish_generate_image", MagicMock())
@patch(f"{MODULE_PATH}.Client")
def test_level(database_mock):
    body = {"user_id": 1234, "server_id": 123, "channel_id": 123}

    request_mock = MagicMock()
    request_mock.get_json.return_value = body
    number_of_users = 1

    database_mock().collection().document().collection().document().get().get.side_effect = get_db_value
    database_mock().collection().document().collection().get.return_value = ["One element"] * number_of_users

    result = level(request_mock)

    assert "Give me a minute, " in result[0]
    assert 200 == result[1]


@patch(f"{MODULE_PATH}.publish_generate_image", MagicMock())
@patch(f"{MODULE_PATH}.Client")
def test_level_mentions(database_mock):
    body = {"user_id": 1234, "server_id": 123, "channel_id": 123, "mentions": ["Archy"]}

    request_mock = MagicMock()
    request_mock.get_json.return_value = body
    number_of_users = 1

    database_mock().collection().document().collection().document().get().get.side_effect = get_db_value
    database_mock().collection().document().collection().get.return_value = ["One element"] * number_of_users
    result = level(request_mock)

    assert "Give me a minute, " in result[0]
    assert 200 == result[1]


@patch(f"{MODULE_PATH}.publish_generate_image", MagicMock())
@patch(f"{MODULE_PATH}.Client")
def test_level_no_level(database_mock):
    body = {"user_id": 1234, "server_id": 123, "channel_id": 123}

    request_mock = MagicMock()
    request_mock.get_json.return_value = body

    database_mock().collection().document().collection().document().get().exists = False
    result = level(request_mock)

    assert (f"... Wait a minute, Who is <@{body['user_id']}>", 200) == result


@patch(f"{MODULE_PATH}.Client", MagicMock())
def test_level_no_user_id():
    body = {"server_id": 123, "channel_id": 123}

    request_mock = MagicMock()
    request_mock.get_json.return_value = body

    result = level(request_mock)

    assert (":|", 200) == result


@patch(f"{MODULE_PATH}.Client", MagicMock())
def test_level_no_body():
    body = None

    request_mock = MagicMock()
    request_mock.get_json.return_value = body

    result = level(request_mock)

    assert (":|", 200) == result


@patch(f"{MODULE_PATH}.PublisherClient")
def test_publish_generate_image(publisher_mock):
    channel_id = 1
    payload = {
        "username": "username",
        "avatar_url": "avatar_url",
        "rank": 1,
        "level": 1,
        "percent": 94,
    }

    data = {"channel_id": channel_id, "payload": payload}
    encoded_data: str = json.dumps(data, indent=2).encode("utf-8")

    publish_generate_image(channel_id, payload)

    assert publisher_mock().method_calls[0].args == (
        "archy-f06ed",
        "generate_level_image",
    )
    assert publisher_mock().method_calls[1][0] == "publish"
    assert publisher_mock().method_calls[1][1][1] == encoded_data
