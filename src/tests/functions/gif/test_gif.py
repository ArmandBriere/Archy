from unittest.mock import MagicMock

from functions.gif.main import gif, liste_gif, git_base


def test_gif_doubt():
    body = {"name": ["doubt"]}

    request_mock = MagicMock()
    request_mock.get_json.return_value = body

    result = gif(request_mock)

    assert result == liste_gif["doubt"]


def test_gif_confusion():
    body = {"name": ["confused"]}

    request_mock = MagicMock()
    request_mock.get_json.return_value = body

    result = gif(request_mock)

    assert result == liste_gif["confused"]


def test_gif_error():
    body = {"name": ["JamesDoe"]}

    request_mock = MagicMock()
    request_mock.get_json.return_value = body

    result = gif(request_mock)

    assert result == git_base
