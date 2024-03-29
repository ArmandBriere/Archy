import json
import os
from typing import Any, Optional, Tuple

import flask
import functions_framework
import requests

DEFAULT_GIF = "https://tenor.com/view/frog-multiply-gif-25342428"
UNKNOWN_GIF = "https://tenor.com/view/bof-i-dont-mind-i-dont-understand-why-jean-dujardin-oss117-gif-20383956"


@functions_framework.http
def gif(request: flask.Request) -> Tuple[str, int]:
    """Return the first gif found with the tenor API."""

    request_json: Optional[Any] = request.get_json(silent=True)
    if request_json:
        params: list = request_json.get("params", [""])

        if len(params) == 0 or params[0] == "":
            return DEFAULT_GIF, 200

        query: str = "+".join(params)

        api_key: str = os.environ["TENOR_API_TOKEN"]
        response: requests.Response = requests.get(
            f"https://tenor.googleapis.com/v2/search?q={query}&key={api_key}&client_key=Archy&limit=1", timeout=5
        )

        return extract_data_from_response(response.status_code, response.content), 200

    return DEFAULT_GIF, 200


def extract_data_from_response(response_status: int, response_content: bytes) -> str:
    """Function that deals with the api request result"""

    if response_status == 200:
        top_gifs = json.loads(response_content)

        try:
            return top_gifs["results"][0]["media_formats"]["gif"]["url"]
        except (KeyError, IndexError):
            return "https://tenor.com/view/404-not-found-error-20th-century-fox-gif-24907780"

    return UNKNOWN_GIF
