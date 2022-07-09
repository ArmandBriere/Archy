# pylint: disable=line-too-long

import json
from datetime import datetime, timedelta
from unittest.mock import MagicMock, patch

import pytest

from functions.exp.main import DATETIME_FORMAT, exp, send_message_to_user, update_user_roles

MODULE_PATH = "functions.exp.main"

GOOD_BODY = {"user_id": "123", "username": "Joe", "avatar_url": "url", "server_id": 123456789, "server_name": "Archy"}


def get_good_db_value(param):  # pragma: no cover
    if param == "level":
        return 1
    if param == "exp_toward_next_level":
        return 0
    if param == "last_message_timestamp":
        return (datetime.now() - timedelta(seconds=60)).strftime(DATETIME_FORMAT)

    return 0


@patch(f"{MODULE_PATH}.Client")
@patch("random.randint")
@patch(f"{MODULE_PATH}.base64")
def test_exp(b64_mock, random_mock, client_mock):

    b64_mock.b64decode.return_value.decode.return_value = GOOD_BODY

    client_mock.return_value.collection.return_value.document.return_value.collection.return_value.document.return_value.get.return_value.get.side_effect = (
        get_good_db_value
    )
    random_mock.return_value = 50

    result = exp(MagicMock(), None)

    assert ("", 200) == result


def get_timeout_timestamp_value(param):  # pragma: no cover
    if param == "last_message_timestamp":
        return (datetime.now() - timedelta(seconds=1)).strftime(DATETIME_FORMAT)

    return 0


@patch(f"{MODULE_PATH}.Client")
@patch(f"{MODULE_PATH}.base64")
def test_exp_timeout(b64_mock, client_mock):

    b64_mock.b64decode.return_value.decode.return_value = GOOD_BODY

    client_mock.return_value.collection.return_value.document.return_value.collection.return_value.document.return_value.get.return_value.get.side_effect = (
        get_timeout_timestamp_value
    )

    result = exp(b64_mock, None)

    assert ("", 200) == result


@pytest.mark.parametrize(
    ("body"),  # Data scheme of the next nested list
    [
        {},
        {
            "user_id": "",
            "username": "",
            "server_id": "",
        },
        {
            "user_id": "user_id",
            "username": "username",
        },
        {
            "username": "username",
            "server_id": "server_id",
        },
        {
            "server_id": "server_id",
            "user_id": "user_id",
        },
    ],
)
@patch(f"{MODULE_PATH}.Client")
@patch("random.randint")
@patch(f"{MODULE_PATH}.base64")
def test_exp_missing_data(b64_mock, random_mock, database_mock, body):

    b64_mock.b64decode.return_value.decode.return_value = body

    database_mock.return_value.collection.return_value.document.return_value.collection.return_value.document.return_value.get.return_value.get.side_effect = (
        get_good_db_value
    )
    random_mock.return_value = 50

    result = exp(b64_mock, None)

    assert ("", 200) == result


@patch(f"{MODULE_PATH}.update_user_roles", MagicMock())
@patch(f"{MODULE_PATH}.send_message_to_user", MagicMock())
@patch(f"{MODULE_PATH}.Client")
@patch("random.randint")
@patch(f"{MODULE_PATH}.base64")
def test_exp_level_up(b64_mock, random_mock, database_mock):

    b64_mock.b64decode.return_value.decode.return_value = GOOD_BODY

    database_mock.return_value.collection.return_value.document.return_value.collection.return_value.document.return_value.get.return_value.get.side_effect = (
        get_good_db_value
    )
    random_mock.return_value = 500
    database_mock.return_value.batch.return_value = MagicMock()

    result = exp(b64_mock, None)

    assert ("", 200) == result
    assert database_mock.return_value.batch.call_count == 1
    assert len(database_mock.return_value.batch.mock_calls) == 6


@patch(f"{MODULE_PATH}.Client")
@patch(f"{MODULE_PATH}.base64")
def test_exp_new_user(b64_mock, database_mock):
    expected_set_value = {
        "total_exp": 0,
        "exp_toward_next_level": 0,
        "level": 0,
        "message_count": 0,
        "last_message_timestamp": datetime.now().strftime(DATETIME_FORMAT),
        "username": GOOD_BODY["username"],
        "avatar_url": GOOD_BODY["avatar_url"],
    }

    b64_mock.b64decode.return_value.decode.return_value = GOOD_BODY

    database_mock.return_value.collection.return_value.document.return_value.collection.return_value.document.return_value.get.return_value.exists = (
        False
    )
    database_mock.return_value.batch.return_value = MagicMock()

    result = exp(b64_mock, None)

    set_value = database_mock.return_value.batch.return_value.method_calls[0][1][1]
    assert ("", 200) == result
    assert set_value == expected_set_value


@patch(f"{MODULE_PATH}.PublisherClient")
def test_send_message_to_user(publisher_mock):
    user_id = 1
    message = "hello"

    data = {"user_id": user_id, "message": message}
    encoded_data: str = json.dumps(data, indent=2).encode("utf-8")

    send_message_to_user(user_id, message)

    assert publisher_mock.return_value.method_calls[0].args == ("archy-f06ed", "private_message_discord")
    assert publisher_mock.return_value.method_calls[1][0] == "publish"
    assert publisher_mock.return_value.method_calls[1][1][1] == encoded_data


@patch(f"{MODULE_PATH}.PublisherClient")
def test_update_user_roles(publisher_mock):
    server_id = 1
    user_id = 1

    data = {"server_id": server_id, "user_id": user_id}
    encoded_data: str = json.dumps(data, indent=2).encode("utf-8")

    update_user_roles(server_id, user_id)

    assert publisher_mock.return_value.method_calls[0].args == ("archy-f06ed", "update_user_role")
    assert publisher_mock.return_value.method_calls[1][0] == "publish"
    assert publisher_mock.return_value.method_calls[1][1][1] == encoded_data
