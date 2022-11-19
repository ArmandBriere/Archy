import flask
import functions_framework

def getChannelName(request):
    request_json = request.get_json(silent=True)
    channelName = request_json.get("server_name", None)
    if channelName.include("#"):
        channelName.replace("#", "")
    return lower(channelName)

@functions_framework.http
def infoCours(request):
    requs
    """This is a template function that show how to send back message."""
    

    request_json: Optional[Any] = request.get_json(silent=True)

    if request_json:
        user_id = request_json.get("user_id", None)
        if user_id:
            return f"Hello Monsieur <@{user_id}>!", 200

    return "Hello Monsieur!", 200
