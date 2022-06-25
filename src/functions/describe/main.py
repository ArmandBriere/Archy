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
        if mentions and mentions[0] == 135048445097410560:
            return "Cette personne est formidable !"

        return f"C'est un bon gros **** ce <@{mentions[0]}> !"
    return f"T'es un bon gros **** ! <@{name}> !"
