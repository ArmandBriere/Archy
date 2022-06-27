from typing import Any, Optional, Tuple

import functions_framework


@functions_framework.http
def hello(request) -> Tuple[str, int]:
    """This is a template function that show how to send back message."""

    request_json: Optional[Any] = request.get_json(silent=True)

    if request_json:
        user_id = request_json.get("user_id", None)
        if user_id:
            return f"Hello <@{user_id}>!", 200

    return "Hello !", 200
