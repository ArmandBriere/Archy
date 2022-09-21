from unittest.mock import patch

from functions.answer.main import POSSIBLE_ANSWERS, answer


@patch("random.choice")
def test_answer(choice_mock):
    choice_mock.return_value = POSSIBLE_ANSWERS[0]

    result = answer(None)

    assert result[0] == POSSIBLE_ANSWERS[0]
    assert result[1] == 200
