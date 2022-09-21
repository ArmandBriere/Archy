from functions.answer.main import POSSIBLE_ANSWERS, answer


def test_hello():
    result = answer({})

    assert result[0] in POSSIBLE_ANSWERS
    assert result[1] == 200
