import os
from unittest.mock import MagicMock, patch

from functions.exp.main import exp, update_user_ranks


def get_db_value(param):  # pragma: no cover
    if param == "level":
        return 1
    if param == "exp_toward_next_level":
        return 0

    return 0


@patch.dict(os.environ, {"GOOGLE_APPLICATION_CREDENTIALS": "{}"})
@patch("firebase_admin.credentials.Certificate", MagicMock())
@patch("firebase_admin.initialize_app", MagicMock())
@patch("firebase_admin.firestore.client")
@patch("random.randint")
def test_exp(random_mock, database_mock):
    body = {"name": "Hello, World!"}

    request_mock = MagicMock()
    request_mock.get_json.return_value = body

    database_mock.return_value.collection.return_value.document.return_value.get.return_value.get.side_effect = (
        get_db_value
    )
    random_mock.return_value = 50

    result = exp(request_mock)

    assert f"Congratz <@{body['name']}>! You have more exp now!" == result


@patch.dict(os.environ, {"GOOGLE_APPLICATION_CREDENTIALS": "{}"})
@patch("firebase_admin.credentials.Certificate", MagicMock())
@patch("firebase_admin.initialize_app", MagicMock())
@patch("firebase_admin.firestore.client")
@patch("random.randint")
def test_exp_level_up(random_mock, database_mock):
    body = {"name": "Hello, World!"}

    request_mock = MagicMock()
    request_mock.get_json.return_value = body

    database_mock.return_value.collection.return_value.document.return_value.get.return_value.get.side_effect = (
        get_db_value
    )
    random_mock.return_value = 500
    database_mock.return_value.batch.return_value = MagicMock()

    result = exp(request_mock)

    assert f"Congratz <@{body['name']}>! You have more exp now!" == result
    assert database_mock.return_value.batch.call_count == 1
    assert len(database_mock.return_value.batch.mock_calls) == 5


@patch.dict(os.environ, {"GOOGLE_APPLICATION_CREDENTIALS": "{}"})
@patch("firebase_admin.credentials.Certificate", MagicMock())
@patch("firebase_admin.initialize_app", MagicMock())
@patch("firebase_admin.firestore.client")
def test_exp_new_user(database_mock):
    body = {"name": "Joe"}
    expected_set_value = {"total_exp": 0, "exp_toward_next_level": 0, "level": 0}

    request_mock = MagicMock()
    request_mock.get_json.return_value = body

    database_mock.return_value.collection.return_value.document.return_value.get.return_value.exists = False
    database_mock.return_value.batch.return_value = MagicMock()

    result = exp(request_mock)

    set_value = database_mock.return_value.batch.return_value.method_calls[0][1][1]
    assert f"Congratz <@{body['name']}>! You have more exp now!" == result
    assert set_value == expected_set_value


@patch("firebase_admin.firestore.client")
def test_update_user_ranks(database_mock):
    mock_users = [
        MagicMock(),
        MagicMock(),
    ]
    database_mock.collection.return_value.order_by.return_value.stream.return_value = mock_users

    update_user_ranks(database_mock)

    assert database_mock.batch.return_value.commit.call_count == 1
    assert database_mock.batch.return_value.update.call_count == len(mock_users)
