from unittest.mock import MagicMock

from functions.answer.main import POSSIBLE_ANSWERS, answer


def test_hello():
    request_mock = MagicMock()

    result = answer(request_mock)

    assert result[0] in POSSIBLE_ANSWERS
    assert result[1] == 200
