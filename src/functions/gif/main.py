import functions_framework

liste_gif = {
    "doubt": "https://tenor.com/view/doubt-press-x-la-noire-meme-x-button-gif-19259237",
    "confused": "https://tenor.com/view/confusion-chicken-gif-11299790",
}

gif_base = "https://tenor.com/view/confusion-chicken-gif-11299790"


@functions_framework.http
def gif(request):
    """HTTP Cloud Function."""
    request_json = request.get_json(silent=True)
    if request_json:
        params = request_json.get("params", None)
        nom_gif = params[0].lower()
        if nom_gif in liste_gif:
            return liste_gif[nom_gif]
        else:
            return gif_base
    return gif_base
