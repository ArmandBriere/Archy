import functions_framework


@functions_framework.http
def decris_moi(request):
    """HTTP Cloud Function."""
    request_json = request.get_json(silent=True)
    if request_json:
        name = request_json.get("name", None)
        mentions = request_json.get("mentions", None)
        if len(mentions) == 0:
            return f"T'es un bon gros pd ! <@{name}> !"
        else:
            print(mentions[0])
            if mentions[0] == 135048445097410560:
                return "Cette personne est formidable !"
            else:
                return f"C'est un bon gros pd ce <@{mentions[0]}> !"
    return ""