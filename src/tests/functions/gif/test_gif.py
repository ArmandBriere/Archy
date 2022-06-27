import json
import os
from unittest.mock import MagicMock, patch

import pytest

from functions.gif.main import DEFAULT_GIF, UNKNOWN_GIF, extract_data_from_response, gif, gifs

MODULE_PATH = "functions.gif.main"


def test_gif_with_empty_body():
    body = {}

    request_mock = MagicMock()
    request_mock.get_json.return_value = body

    result = gif(request_mock)

    assert result == (DEFAULT_GIF, 200)


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

    assert result == (gifs[body["params"][0]], 200)


@patch.dict(os.environ, {"TENOR_API_TOKEN": "TEST"}, clear=True)
@patch(f"{MODULE_PATH}.requests")
def test_gif_tenor_search(http_request_mock):
    body = {"params": ["JamesDoe"]}

    request_mock = MagicMock()
    request_mock.get_json.return_value = body

    result = gif(request_mock)

    exp_result = (UNKNOWN_GIF, 200)

    assert exp_result == result
    assert http_request_mock.get.call_count == 1
    assert os.environ["TENOR_API_TOKEN"] in http_request_mock.get.call_args[0][0]


def test_gif_empty_params():
    body = {"params": []}

    request_mock = MagicMock()
    request_mock.get_json.return_value = body

    result = gif(request_mock)

    assert result == (DEFAULT_GIF, 200)


def test_gif_empty_string_params():
    body = {"params": [""]}

    request_mock = MagicMock()
    request_mock.get_json.return_value = body

    result = gif(request_mock)

    assert result == (DEFAULT_GIF, 200)


def test_extract_data_correct_tenor_response():
    expected_result = "https://c.tenor.com/HvtIOMNuwhYAAAAC/wat-what.gif"
    response_content_dict = {
        "results": [
            {
                "media_formats": {
                    "gif": {
                        "url": expected_result,
                    }
                }
            }
        ]
    }
    response_bytes = json.dumps(response_content_dict).encode("utf-8")

    api_status = 200

    assert expected_result == extract_data_from_response(api_status, response_bytes)


def test_extract_data_empty_tenor_response():
    response_content_dict = {}
    response_bytes = json.dumps(response_content_dict).encode("utf-8")
    api_status = 200

    expected_result = "https://tenor.com/view/404-not-found-error-20th-century-fox-gif-24907780"

    result = extract_data_from_response(api_status, response_bytes)

    assert expected_result == result


def test_extract_data_status_code_not_200():
    response_content_dict = {}
    response_bytes = json.dumps(response_content_dict).encode("utf-8")
    api_status = 503

    result = extract_data_from_response(api_status, response_bytes)

    assert UNKNOWN_GIF == extract_data_from_response(api_status, result)
