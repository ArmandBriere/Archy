import os
from unittest.mock import MagicMock, patch

from functions.level.main import level


def get_db_value(param):  # pragma: no cover
    if param == "level":
        return 1
    if param == "rank":
        return 1

    return 0


@patch.dict(os.environ, {"GOOGLE_APPLICATION_CREDENTIALS": "{}"})
@patch("firebase_admin.credentials.Certificate", MagicMock())
@patch("firebase_admin.initialize_app", MagicMock())
@patch("firebase_admin.firestore.client")
def test_exp(database_mock):
    body = {"name": "Hello, World!"}

    request_mock = MagicMock()
    request_mock.get_json.return_value = body
    current_level = get_db_value("level")
    current_rank = get_db_value("rank")
    number_of_users = 1

    database_mock.return_value.collection.return_value.document.return_value.get.return_value.get.side_effect = (
        get_db_value
    )
    database_mock.return_value.collection.return_value.get.return_value = ["One element"] * number_of_users

    result = level(request_mock)

    assert f"<@{body['name']}> is level {current_level}! Rank {current_rank}/{number_of_users}" == result


@patch.dict(os.environ, {"GOOGLE_APPLICATION_CREDENTIALS": "{}"})
@patch("firebase_admin.credentials.Certificate", MagicMock())
@patch("firebase_admin.initialize_app", MagicMock())
@patch("firebase_admin.firestore.client")
def test_exp_mentions(database_mock):
    body = {"name": "Hello, World!", "mentions": ["Archy"]}

    request_mock = MagicMock()
    request_mock.get_json.return_value = body
    current_level = get_db_value("level")
    current_rank = get_db_value("rank")
    number_of_users = 1

    database_mock.return_value.collection.return_value.document.return_value.get.return_value.get.side_effect = (
        get_db_value
    )
    database_mock.return_value.collection.return_value.get.return_value = ["One element"] * number_of_users

    result = level(request_mock)

    assert f"<@{body['mentions'][0]}> is level {current_level}! Rank {current_rank}/{number_of_users}" == result


@patch.dict(os.environ, {"GOOGLE_APPLICATION_CREDENTIALS": "{}"})
@patch("firebase_admin.credentials.Certificate", MagicMock())
@patch("firebase_admin.initialize_app", MagicMock())
@patch("firebase_admin.firestore.client")
def test_exp_no_level(database_mock):
    body = {"name": "Hello, World!"}

    request_mock = MagicMock()
    request_mock.get_json.return_value = body

    database_mock.return_value.collection.return_value.document.return_value.get.return_value.exists = False

    result = level(request_mock)

    assert f"... Wait a minute, Who is <@{body['name']}>" == result


@patch.dict(os.environ, {"GOOGLE_APPLICATION_CREDENTIALS": "{}"})
@patch("firebase_admin.credentials.Certificate", MagicMock())
@patch("firebase_admin.initialize_app", MagicMock())
def test_exp_no_name():
    body = {"ranom": "value"}

    request_mock = MagicMock()
    request_mock.get_json.return_value = body

    result = level(request_mock)

    assert ":|" == result


@patch.dict(os.environ, {"GOOGLE_APPLICATION_CREDENTIALS": "{}"})
@patch("firebase_admin.credentials.Certificate", MagicMock())
@patch("firebase_admin.initialize_app", MagicMock())
def test_exp_no_body():
    body = None

    request_mock = MagicMock()
    request_mock.get_json.return_value = body

    result = level(request_mock)

    assert ":|" == result
