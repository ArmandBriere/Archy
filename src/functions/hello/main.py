import functions_framework
from typing import Any, Optional


@functions_framework.http
def hello(request) -> tuple[str, int]:
    """This is a template function that show how to send back message."""

    request_json: Optional[Any] = request.get_json(silent=True)

    if request_json:
        name = request_json.get("name", None)
        if name:
            return f"Hello <@{name}>!"

    return "Hello !", 200
