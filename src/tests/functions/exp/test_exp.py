import os
from unittest.mock import MagicMock, patch

from functions.exp.main import exp


def get_db_value(param):
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
