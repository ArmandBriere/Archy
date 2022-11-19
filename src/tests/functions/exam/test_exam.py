from unittest.mock import MagicMock, patch

import pytest

from functions.exam.main import exam

MODULE_PATH = "functions.exam.main"


def test_exam():
    body = {
        "channel_name": "inf3080"
    }

    request_mock = MagicMock()
    request_mock.get_json.return_value = body

    result = exam(request_mock)
    expected = "Vos exams: \n Intra: 29 oct. 09:30 à 12:30 \n Finale: 17 déc. 09:30 à 12:30"

    assert expected == result

def test_exam_empty_param():
    body = {
        "channel_name": ""
    }

    request_mock = MagicMock()
    request_mock.get_json.return_value = body

    result = exam(request_mock)
    expected = "Je n'ai rien trouvé"

    assert expected == result

@patch(f"{MODULE_PATH}.requests")
def test_exam_empty_response(http_request_mock):
    body = {
        "channel_name": "inf3080"
    }

    request_mock = MagicMock()
    request_mock.get_json.return_value = body

    result = exam(request_mock)
    expected = "Je n'ai rien trouvé"

    assert expected == result
    assert http_request_mock.get.call_count == 1

def test_exam_inexistant_course():
    body = {
        "channel_name": "xxxx"
    }

    request_mock = MagicMock()
    request_mock.get_json.return_value = body

    result = exam(request_mock)
    expected = "Je n'ai rien trouvé"

    assert expected == result