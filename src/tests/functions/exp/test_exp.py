# pylint: disable=line-too-long

import os
from datetime import datetime, timedelta
from unittest.mock import MagicMock, patch

from functions.exp.main import DATETIME_FORMAT, exp, update_user_ranks

MODULE_PATH = "functions.exp.main"


def get_db_value(param):  # pragma: no cover
    if param == "level":
        return 1
    if param == "exp_toward_next_level":
        return 0
    if param == "last_message_timestamp":
        return (datetime.now() - timedelta(seconds=60)).strftime(DATETIME_FORMAT)

    return 0


@patch.dict(os.environ, {"GOOGLE_APPLICATION_CREDENTIALS": "{}"})
@patch("firebase_admin.credentials.Certificate", MagicMock())
@patch("firebase_admin.initialize_app", MagicMock())
@patch("firebase_admin.firestore.client")
@patch("random.randint")
def test_exp(random_mock, database_mock):
    body = {"user_id": "Hello, World!"}

    request_mock = MagicMock()
    request_mock.get_json.return_value = body

    database_mock.return_value.collection.return_value.document.return_value.collection.return_value.document.return_value.get.return_value.get.side_effect = (
        get_db_value
    )
    random_mock.return_value = 50

    result = exp(request_mock)

    assert f"Congratz <@{body['user_id']}>! You have more exp now!" == result


@patch.dict(os.environ, {"GOOGLE_APPLICATION_CREDENTIALS": "{}"})
@patch("firebase_admin.credentials.Certificate", MagicMock())
@patch("firebase_admin.initialize_app", MagicMock())
@patch(f"{MODULE_PATH}.send_message_to_user", MagicMock())
@patch("firebase_admin.firestore.client")
@patch("random.randint")
def test_exp_level_up(random_mock, database_mock):
    body = {"user_id": "Hello, World!"}

    request_mock = MagicMock()
    request_mock.get_json.return_value = body

    database_mock.return_value.collection.return_value.document.return_value.collection.return_value.document.return_value.get.return_value.get.side_effect = (
        get_db_value
    )
    random_mock.return_value = 500
    database_mock.return_value.batch.return_value = MagicMock()

    result = exp(request_mock)

    assert f"Congratz <@{body['user_id']}>! You have more exp now!" == result
    assert database_mock.return_value.batch.call_count == 1
    assert len(database_mock.return_value.batch.mock_calls) == 5


@patch.dict(os.environ, {"GOOGLE_APPLICATION_CREDENTIALS": "{}"})
@patch("firebase_admin.credentials.Certificate", MagicMock())
@patch("firebase_admin.initialize_app", MagicMock())
@patch("firebase_admin.firestore.client")
def test_exp_new_user(database_mock):
    body = {"user_id": "123", "username": "Joe", "avatar_url": "url"}
    expected_set_value = {
        "total_exp": 0,
        "exp_toward_next_level": 0,
        "level": 0,
        "rank": 1,
        "last_message_timestamp": datetime.now().strftime(DATETIME_FORMAT),
        "username": body["username"],
        "avatar_url": body["avatar_url"],
    }

    request_mock = MagicMock()
    request_mock.get_json.return_value = body

    database_mock.return_value.collection.return_value.document.return_value.collection.return_value.document.return_value.get.return_value.exists = (
        False
    )
    database_mock.return_value.batch.return_value = MagicMock()

    result = exp(request_mock)

    set_value = database_mock.return_value.batch.return_value.method_calls[0][1][1]
    assert f"Congratz <@{body['user_id']}>! You have more exp now!" == result
    assert set_value == expected_set_value


@patch("firebase_admin.firestore.client")
def test_update_user_ranks(database_mock):
    mock_users = [
        MagicMock(),
        MagicMock(),
    ]
    database_mock.collection.return_value.order_by.return_value.stream.return_value = mock_users
    batch_mock = database_mock.batch.return_value = MagicMock()

    update_user_ranks(database_mock, batch_mock)

    assert batch_mock.commit.call_count == 0
    assert batch_mock.update.call_count == len(mock_users)
