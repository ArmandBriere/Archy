from unittest.mock import MagicMock, patch

from functions.frogeOfTheDay.main import get_all_channels, publish_froge_of_the_day

MODULE_PATH = "functions.frogeOfTheDay.main"


def get_active_channel_id(param):  # pragma: no cover
    if param == "active":
        return True
    if param == "channel_id":
        return "123456789"
    return 0


def get_inactive_channel_id(param):  # pragma: no cover
    if param == "active":
        return False
    if param == "channel_id":
        return "123456789"
    return 0


@patch(f"{MODULE_PATH}.Client")
def test_get_all_channels_active(database_mock):
    server_count = 3

    server = MagicMock()
    server.collection.return_value.document.return_value.get.side_effect = get_active_channel_id
    database_mock.return_value.collection.return_value.stream.return_value = [server] * server_count

    result = get_all_channels()

    assert result == ["123456789"] * server_count


@patch(f"{MODULE_PATH}.Client")
def test_get_all_channels_inactive(database_mock):
    server_count = 3

    server = MagicMock()
    server.collection.return_value.document.return_value.get.side_effect = get_inactive_channel_id
    database_mock.return_value.collection.return_value.stream.return_value = [server] * server_count

    result = get_all_channels()

    assert not result


@patch(f"{MODULE_PATH}.publish_message", MagicMock())
@patch(f"{MODULE_PATH}.generate_froge_of_the_day", MagicMock())
@patch(f"{MODULE_PATH}.print")
@patch(f"{MODULE_PATH}.get_all_channels")
def test_publish_froge_of_the_day(get_all_channels_mock, print_mock):
    get_all_channels_mock.return_value = ["123"]

    assert not publish_froge_of_the_day(None, None)
    assert print_mock.call_count == 1
    assert print_mock.call_args[0][0] == "Start"


@patch(f"{MODULE_PATH}.publish_message", MagicMock())
@patch(f"{MODULE_PATH}.generate_froge_of_the_day", MagicMock())
@patch(f"{MODULE_PATH}.print")
@patch(f"{MODULE_PATH}.get_all_channels")
def test_publish_froge_of_the_day_no_channels(get_all_channels_mock, print_mock):
    get_all_channels_mock.return_value = []

    assert not publish_froge_of_the_day(None, None)
    assert print_mock.call_count == 2
    assert print_mock.call_args_list[0][0][0] == "Start"
    assert print_mock.call_args_list[1][0][0] == "Exit: No channels found"
