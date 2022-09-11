import os
from unittest.mock import MagicMock, Mock, mock_open, patch

import requests

from functions.meme.main import NO_EMOJI, UNSUPORTED_MEME, USAGE_GUIDE, meme

MODULE_PATH = "functions.meme.main"


@patch(f"{MODULE_PATH}.open", mock_open(read_data="{}"), create=True)
def test_meme_with_empty_body():
    body = {}

    request_mock = MagicMock()
    request_mock.get_json.return_value = body

    result = meme(request_mock)

    assert result == (USAGE_GUIDE, 200)


@patch.dict(os.environ, {"IMGFLIP_API_USERNAME": "TEST", "IMGFLIP_API_PASSWORD": "TEST"}, clear=True)
@patch(f"{MODULE_PATH}.open", mock_open(read_data='{"TestMeme": "TestID"}'), create=True)
@patch.object(requests, "post")
def test_meme_imgflip_api_request_fail(post_mock: Mock):
    body = {"params": ["TestMeme", "TestTopText", "TestBottomText"]}

    response_mock = Mock()
    post_mock.return_value = response_mock
    response_mock.ok = False

    request_mock = MagicMock()
    request_mock.get_json.return_value = body

    result = meme(request_mock)

    post_mock.assert_called_once()
    assert result == (NO_EMOJI, 200)


@patch.dict(os.environ, {"IMGFLIP_API_USERNAME": "TEST", "IMGFLIP_API_PASSWORD": "TEST"}, clear=True)
@patch(f"{MODULE_PATH}.open", mock_open(read_data='{"TestMeme": "TestID"}'), create=True)
@patch.object(requests, "post")
def test_meme_imgflip_api_fail(post_mock: Mock):
    body = {"params": ["TestMeme", "TestTopText", "TestBottomText"]}

    response_mock = Mock()
    post_mock.return_value = response_mock
    response_mock.json.return_value = {"success": False}

    request_mock = MagicMock()
    request_mock.get_json.return_value = body

    result = meme(request_mock)

    post_mock.assert_called_once()
    assert result == (NO_EMOJI, 200)


@patch(f"{MODULE_PATH}.open", mock_open(read_data="{}"), create=True)
def test_unsuported_meme():
    body = {"params": ["TestMeme", "TestTopText", "TestBottomText"]}

    request_mock = MagicMock()
    request_mock.get_json.return_value = body

    result = meme(request_mock)

    assert result == (UNSUPORTED_MEME, 200)


@patch(f"{MODULE_PATH}.open", mock_open(read_data="{}"), create=True)
def test_meme_empty_params():
    body = {"params": []}

    request_mock = MagicMock()
    request_mock.get_json.return_value = body

    result = meme(request_mock)

    assert result == (USAGE_GUIDE, 200)


@patch(f"{MODULE_PATH}.open", mock_open(read_data="{}"), create=True)
def test_meme_empty_string_params():
    body = {"params": [""]}

    request_mock = MagicMock()
    request_mock.get_json.return_value = body

    result = meme(request_mock)

    assert result == (USAGE_GUIDE, 200)
