import os
from unittest.mock import MagicMock, patch

from functions.exp.main import exp


@patch.dict(os.environ, {"GOOGLE_APPLICATION_CREDENTIALS": "{}"})
@patch("firebase_admin.firestore.client", MagicMock())
@patch("firebase_admin.credentials.Certificate", MagicMock())
@patch("firebase_admin.initialize_app", MagicMock())
def test_exp():
    body = {"name": "Hello, World!"}

    request_mock = MagicMock()
    request_mock.get_json.return_value = body

    result = exp(request_mock)

    assert f"Congratz <@{body['name']}>! You have more exp now!" == result
