import json
from unittest.mock import MagicMock

from functions.insult.main import BASE_INSULT, get_the_insult, insult


def test_insult_empty_body():
    body = {}

    request_mock = MagicMock()
    request_mock.get_json.return_value = body

    result = insult(request_mock)

    assert result == (BASE_INSULT, 200)


def test_insult_no_mentions():
    body = {"mentions": []}

    request_mock = MagicMock()
    request_mock.get_json.return_value = body

    result = insult(request_mock)

    assert "You are" in result[0]
    assert 200 == result[1]


def test_insult_one_mention():
    body = {"mentions": ["1111111111"]}

    request_mock = MagicMock()
    request_mock.get_json.return_value = body

    result = insult(request_mock)

    assert "1111111111" in result[0]
    assert len("1111111111") < len(result[0])
    assert 200 == result[1]


def test_insult_mult_mentions():
    body = {"mentions": ["1111111111", "2222222222", "3333333333"]}

    request_mock = MagicMock()
    request_mock.get_json.return_value = body

    result = insult(request_mock)

    assert "1111111111" in result[0]
    assert "2222222222" in result[0]
    assert "3333333333" in result[0]
    assert (3 * len("3333333333")) < len(result[0])
    assert 200 == result[1]


def test_get_the_insult_bad_code():
    response_content_dict = {}
    response_bytes = json.dumps(response_content_dict).encode("utf-8")
    api_status = 404

    expected_result = "is that an Archy reference?"

    result = get_the_insult(api_status, response_bytes)

    assert result == expected_result


def test_get_the_insult_bad_api_answer():
    response_content_dict = {}
    response_bytes = json.dumps(response_content_dict).encode("utf-8")
    api_status = 200

    result = get_the_insult(api_status, response_bytes)

    assert BASE_INSULT == result
