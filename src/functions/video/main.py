import json
import os
from typing import Any, Optional, Tuple

import flask
import functions_framework
import requests

DEFAULT_VIDEO = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
UNKNOWN_VIDEO = "https://www.youtube.com/watch?v=bnmAi53H520"
NOT_FOUND_VID = "https://www.youtube.com/watch?v=TSXXi2kvl_0"


@functions_framework.http
def video(request: flask.Request) -> Tuple[str, int]:
    """Return the first video found with the youtube data API."""

    request_json: Optional[Any] = request.get_json(silent=True)
    if request_json:
        params: list = request_json.get("params", [""])

        if len(params) == 0 or params[0] == "":
            return DEFAULT_VIDEO, 200

        query: str = "+".join(params)
        api_key: str = os.environ["YOUTUBE_API_TOKEN"]
        # api_key: str = "AIzaSyDuNX5ekco-rYgAAzuHjAznfVr6r0Hjv8E"
        response: requests.Response = requests.get(
            f"https://www.googleapis.com/youtube/v3/search?key={api_key}&q={query}&part=snippet&type=video&maxResults=1"
        )

        return extract_data_from_response(response.status_code, response.content), 200

    return DEFAULT_VIDEO, 200


def extract_data_from_response(response_status: int, response_content: bytes) -> str:
    """Function that deals with the api request result"""

    if response_status == 200:
        top_vid = json.loads(response_content)

        try:
            vid_id = top_vid["items"][0]["id"]["videoId"]
            return "https://youtu.be/" + vid_id
        except (KeyError, IndexError):
            return NOT_FOUND_VID

    return UNKNOWN_VIDEO
