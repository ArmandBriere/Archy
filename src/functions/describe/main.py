from typing import Any, Optional

import functions_framework


@functions_framework.http
def describe(request):
    """Describe the user in mentions or the author."""

    request_json: Optional[Any] = request.get_json(silent=True)

    if request_json:
        name = request_json.get("name", None)
        mentions = request_json.get("mentions", None)

        # Special user are protected. This will go with firebase in the future
        if mentions:
            if mentions[0] == 135048445097410560:
                return "This person is awesome!"
            return f"<@{mentions[0]}> is a big ****!", 200

        return f"You are a big ****! <@{name}>", 200

    return "I don't even know who you are!", 200
