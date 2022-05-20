import os
from unittest.mock import MagicMock, patch

from functions.exp.main import exp


@patch.dict(os.environ, {"GOOGLE_APPLICATION_CREDENTIALS": "{}"})
@patch("firebase_admin.firestore.client")
@patch("firebase_admin.credentials.Certificate")
@patch("firebase_admin.initialize_app")
def test_exp(_initialize_app_mock, _certificate_mock, _firestore_client_mock):
    body = {"name": "Hello, World!"}

    request_mock = MagicMock()
    request_mock.get_json.return_value = body

    result = exp(request_mock)

    assert f"Congratz <@{body['name']}>! You have more exp now!" == result
