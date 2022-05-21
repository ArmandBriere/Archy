import functions_framework


@functions_framework.http
def hello(request):
    """HTTP Cloud Function."""
    request_json = request.get_json(silent=True)
    if request_json:
        name = request_json.get("name", None)
        if name:
            return f"Hello <@{name}>!"
    return "Hello !"
