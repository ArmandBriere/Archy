from typing import Any, Optional, Tuple

import flask
import functions_framework
import requests

DEFAULT_IMG = "https://http.cat/418"
BASE_URL = "https://http.cat/"
ERROR_URL = "https://http.cat/404"


@functions_framework.http
def http(request: flask.Request) -> Tuple[str, int]:
    """Return an image describing the given http code using the http cats api."""

    request_json: Optional[Any] = request.get_json(silent=True)
    if request_json:
        params: list = request_json.get("params", [""])

        if len(params) == 0 or params[0] == "":
            return DEFAULT_IMG, 200

        url_result = f"{BASE_URL}{params[0]}"

        response: requests.Response = requests.get(url_result, timeout=5)
        normal_code = [200, 304]

        if response.status_code not in normal_code:
            return ERROR_URL, 200

        return url_result, 200
    return ERROR_URL, 200
