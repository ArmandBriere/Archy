import os
from unittest.mock import MagicMock, patch

import pytest

from functions.gif.main import DEFAULT_GIF, UNKNOWN_GIF, get_gif_from_api, gif, gifs


@pytest.mark.parametrize(
    ("body"),
    [
        {"params": ["doubt"]},
        {"params": ["confused"]},
    ],
)
@patch.dict(os.environ, {"TENOR_API_TOKEN": "{}"})
def test_gif_with_param(body):
    """Test known keyword"""
    request_mock = MagicMock()
    request_mock.get_json.return_value = body

    result = gif(request_mock)

    assert result == (gifs[body["params"][0]], 200)


@patch.dict(os.environ, {"TENOR_API_TOKEN": "{}"})
def test_gif_search():
    """Test unknown keyword (cover)"""
    body = {"params": ["JamesDoe"]}

    request_mock = MagicMock()
    request_mock.get_json.return_value = body

    result = gif(request_mock)

    exp_result = (UNKNOWN_GIF, 200)

    assert exp_result == result


@patch.dict(os.environ, {"TENOR_API_TOKEN": "{}"})
def test_gif_no_body():
    """Test no json"""
    body = {}

    request_mock = MagicMock()
    request_mock.get_json.return_value = body

    result = gif(request_mock)

    assert result == (DEFAULT_GIF, 200)


@patch.dict(os.environ, {"TENOR_API_TOKEN": "{}"})
def test_gif_empty_params():
    """Test no keyword"""
    body = {"params": []}

    request_mock = MagicMock()
    request_mock.get_json.return_value = body

    result = gif(request_mock)

    assert result == (DEFAULT_GIF, 200)


def test_success_200():
    """Test success api call"""
    api_request_json = """{"results": [
                {
                    "media_formats": {
                    "gif": {
                        "url": "https://c.tenor.com/HvtIOMNuwhYAAAAC/wat-what.gif",
                        "duration": 0,
                        "preview": "",
                        "dims": [
                        436,
                        498
                        ],
                        "size": 7986816
                    }
                    }
                }
                ]
            }"""

    expected_result = "https://c.tenor.com/HvtIOMNuwhYAAAAC/wat-what.gif"

    api_status = 200

    assert expected_result == get_gif_from_api(api_status, api_request_json)


def test_success_200_bad_json():
    """Test bad json format api"""
    api_request_json = """{ }"""

    expected_result = "https://tenor.com/view/im-dead-vanilla-patay-na-ako-dead-nako-patay-ako-gif-22020482"

    api_status = 200

    assert expected_result == get_gif_from_api(api_status, api_request_json)


def test_fail_not_200():
    """Test API request failure"""
    api_request_json = """{ }"""

    api_status = 503

    assert UNKNOWN_GIF == get_gif_from_api(api_status, api_request_json)
