import os
from unittest.mock import MagicMock, patch

from functions.level.main import level


@patch.dict(os.environ, {"GOOGLE_APPLICATION_CREDENTIALS": "{}"})
@patch("firebase_admin.credentials.Certificate", MagicMock())
@patch("firebase_admin.initialize_app", MagicMock())
@patch("firebase_admin.firestore.client")
def test_exp(database_mock):
    body = {"name": "Hello, World!"}

    request_mock = MagicMock()
    request_mock.get_json.return_value = body
    current_level = 1

    database_mock.return_value.collection.return_value.document.return_value.get.return_value.get.return_value = (
        current_level
    )

    result = level(request_mock)

    assert f"<@{body['name']}> is level {current_level}!" == result


@patch.dict(os.environ, {"GOOGLE_APPLICATION_CREDENTIALS": "{}"})
@patch("firebase_admin.credentials.Certificate", MagicMock())
@patch("firebase_admin.initialize_app", MagicMock())
@patch("firebase_admin.firestore.client")
def test_exp_mentions(database_mock):
    body = {"name": "Hello, World!", "mentions": ["Archy"]}

    request_mock = MagicMock()
    request_mock.get_json.return_value = body
    current_level = 1

    database_mock.return_value.collection.return_value.document.return_value.get.return_value.get.return_value = (
        current_level
    )

    result = level(request_mock)

    assert f"<@{body['mentions'][0]}> is level {current_level}!" == result


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
