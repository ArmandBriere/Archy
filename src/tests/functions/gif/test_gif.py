from unittest.mock import MagicMock

from functions.gif.main import gif, gifs, unknown_gif, default_gif


def test_gif_doubt():
    body = {"params": ["doubt"]}

    request_mock = MagicMock()
    request_mock.get_json.return_value = body

    result = gif(request_mock)

    assert result == gifs["doubt"]


def test_gif_confusion():
    body = {"params": ["confused"]}

    request_mock = MagicMock()
    request_mock.get_json.return_value = body

    result = gif(request_mock)

    assert result == gifs["confused"]


def test_gif_error():
    body = {"params": ["JamesDoe"]}

    request_mock = MagicMock()
    request_mock.get_json.return_value = body

    result = gif(request_mock)

    assert result == unknown_gif


def test_gif_no_params():
    body = {}

    request_mock = MagicMock()
    request_mock.get_json.return_value = body

    result = gif(request_mock)

    assert result == default_gif
