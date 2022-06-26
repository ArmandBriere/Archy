# pylint: disable=line-too-long

from unittest.mock import MagicMock, patch

from functions.level.main import level

MODULE_PATH = "functions.level.main"


def get_db_value(param):  # pragma: no cover
    if param == "level":
        return 1
    if param == "rank":
        return 1

    return 0


@patch(f"{MODULE_PATH}.Client")
def test_exp(database_mock):
    body = {"user_id": 1234}

    request_mock = MagicMock()
    request_mock.get_json.return_value = body
    current_level = get_db_value("level")
    current_rank = get_db_value("rank")
    number_of_users = 1

    database_mock.return_value.collection.return_value.document.return_value.collection.return_value.document.return_value.get.return_value.get.side_effect = (
        get_db_value
    )
    database_mock.return_value.collection.return_value.document.return_value.collection.return_value.get.return_value = [
        "One element"
    ] * number_of_users

    result = level(request_mock)

    assert (f"<@{body['user_id']}> is level {current_level}! Rank {current_rank}", 200) == result


@patch(f"{MODULE_PATH}.Client")
def test_exp_mentions(database_mock):
    body = {"user_id": "Hello, World!", "mentions": ["Archy"]}

    request_mock = MagicMock()
    request_mock.get_json.return_value = body
    current_level = get_db_value("level")
    current_rank = get_db_value("rank")
    number_of_users = 1

    database_mock.return_value.collection.return_value.document.return_value.collection.return_value.document.return_value.get.return_value.get.side_effect = (
        get_db_value
    )
    database_mock.return_value.collection.return_value.document.return_value.collection.return_value.get.return_value = [
        "One element"
    ] * number_of_users
    result = level(request_mock)

    assert (f"<@{body['mentions'][0]}> is level {current_level}! Rank {current_rank}", 200) == result


@patch(f"{MODULE_PATH}.Client")
def test_exp_no_level(database_mock):
    body = {"user_id": 1234}

    request_mock = MagicMock()
    request_mock.get_json.return_value = body

    database_mock.return_value.collection.return_value.document.return_value.collection.return_value.document.return_value.get.return_value.exists = (
        False
    )
    result = level(request_mock)

    assert (f"... Wait a minute, Who is <@{body['user_id']}>", 200) == result


@patch(f"{MODULE_PATH}.Client", MagicMock())
def test_exp_no_name():
    body = {"random": "value"}

    request_mock = MagicMock()
    request_mock.get_json.return_value = body

    result = level(request_mock)

    assert (":|", 200) == result


@patch(f"{MODULE_PATH}.Client", MagicMock())
def test_exp_no_body():
    body = None

    request_mock = MagicMock()
    request_mock.get_json.return_value = body

    result = level(request_mock)

    assert (":|", 200) == result
