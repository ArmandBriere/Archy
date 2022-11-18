import json
import os
from unittest.mock import MagicMock, patch

from functions.video.main import DEFAULT_VIDEO, NOT_FOUND_VID, UNKNOWN_VIDEO, extract_data_from_response, video

MODULE_PATH = "functions.video.main"


def test_video_with_empty_body():
    body = {}

    request_mock = MagicMock()
    request_mock.get_json.return_value = body

    result = video(request_mock)

    assert result == (DEFAULT_VIDEO, 200)


@patch.dict(os.environ, {"YOUTUBE_API_TOKEN": "TEST"}, clear=True)
@patch(f"{MODULE_PATH}.requests")
def test_gif_tenor_search(http_request_mock):
    body = {"params": ["JamesDoe"]}

    request_mock = MagicMock()
    request_mock.get_json.return_value = body

    result = video(request_mock)

    exp_result = (UNKNOWN_VIDEO, 200)

    assert exp_result == result
    assert http_request_mock.get.call_count == 1
    assert os.environ["YOUTUBE_API_TOKEN"] in http_request_mock.get.call_args[0][0]


def test_video_empty_params():
    body = {"params": []}

    request_mock = MagicMock()
    request_mock.get_json.return_value = body

    result = video(request_mock)

    assert result == (DEFAULT_VIDEO, 200)


def test_video_empty_string_params():
    body = {"params": [""]}

    request_mock = MagicMock()
    request_mock.get_json.return_value = body

    result = video(request_mock)

    assert result == (DEFAULT_VIDEO, 200)


def test_extract_data_correct_tenor_response():
    expected_result = "9bZkp7q19f0"
    response_content_dict = {
        "items": [
            {
                "id": {
                    "videoId": expected_result,
                }
            }
        ]
    }
    response_bytes = json.dumps(response_content_dict).encode("utf-8")

    api_status = 200

    expected_result_comp = "https://youtu.be/" + expected_result
    assert expected_result_comp == extract_data_from_response(api_status, response_bytes)


def test_extract_data_empty_tenor_response():
    response_content_dict = {}
    response_bytes = json.dumps(response_content_dict).encode("utf-8")
    api_status = 200

    expected_result = NOT_FOUND_VID

    result = extract_data_from_response(api_status, response_bytes)

    assert expected_result == result


def test_extract_data_status_code_not_200():
    response_content_dict = {}
    response_bytes = json.dumps(response_content_dict).encode("utf-8")
    api_status = 503

    result = extract_data_from_response(api_status, response_bytes)

    assert UNKNOWN_VIDEO == extract_data_from_response(api_status, result)
