from flask import escape
import functions_framework


@functions_framework.http
def hello(request):
    """HTTP Cloud Function."""
    request_json = request.get_json(silent=True)
    name = ""
    if request_json:
        name = request_json.get("name", "... wait, WHO ARE YOU?")

    return "Hello <@{}>!".format(escape(name))
