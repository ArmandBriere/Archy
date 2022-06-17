import functions_framework


@functions_framework.http
def hello(request):
    """Simple hello back to the author of the message."""

    request_json = request.get_json(silent=True)

    if request_json:
        name = request_json.get("name", None)
        if name:
            return f"Hello <@{name}>!"

    return "Hello !"
