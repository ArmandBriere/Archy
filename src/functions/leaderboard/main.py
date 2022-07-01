from typing import Any, Optional, Tuple

import flask
import functions_framework

BASE_URL = "https://archybot.web.app/leaderboard/"


@functions_framework.http
def leaderboard(request: flask.Request) -> Tuple[str, int]:  # pylint: disable=W0622
    """Return the current server leaderboard url."""

    request_json: Optional[Any] = request.get_json(silent=True)
    if request_json:
        server_id = request_json.get("server_id", None)

        if not server_id:
            print("Exit: Missing data in payload")
            return "", 200

        return f"{BASE_URL}/{server_id}"

    return "", 200
