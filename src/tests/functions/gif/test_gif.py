from unittest.mock import MagicMock

import pytest

from functions.gif.main import DEFAULT_GIF, gif, gifs


@pytest.mark.parametrize(
    ("body"),
    [
        {"params": ["doubt"]},
        {"params": ["confused"]},
    ],
)
def test_gif_with_param(body):
    request_mock = MagicMock()
    request_mock.get_json.return_value = body

    result = gif(request_mock)

    assert result == gifs[body["params"][0]]


def test_gif_recherche():
    body = {"params": ["JamesDoe"]}

    request_mock = MagicMock()
    request_mock.get_json.return_value = body

    result = gif(request_mock)
    url_part = "https://media.tenor.com/"

    assert url_part in result


def test_gif_no_body():
    body = {}

    request_mock = MagicMock()
    request_mock.get_json.return_value = body

    result = gif(request_mock)

    assert result == DEFAULT_GIF


def test_gif_empty_params():
    body = {"params": []}

    request_mock = MagicMock()
    request_mock.get_json.return_value = body

    result = gif(request_mock)

    assert result == DEFAULT_GIF
