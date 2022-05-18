# https://docs.pytest.org/en/7.1.x/


def inc(test_value: int):
    return test_value + 1


def test_answer():
    assert inc(4) == 5
