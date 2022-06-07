import functions_framework

liste_gif = {
    "doubt": """https://images-ext-2.discordapp.net/external/
            bZOS_Lss71I5JmMKH0I7yupkLVXrU4lWcxTJ2w2ONRM/
            https/media.tenor.com/0KEvxoQb5a4AAAPo/
            doubt-press-x.mp4""",
    "confused": """https://images-ext-2.discordapp.net/
            external/WZJBGDxw62KT6tHXgbZpvr6NmBP91h10uurhfl6GPPI/
            https/media.tenor.com/JLwgRWNpmYYAAAPo/
            confusion-chicken.mp4"""
}

gif_base = """https://images-ext-1.discordapp.net/
        external/xeuVGypBTU5pis9a37wCSxjmAvbwqzUrj-1y4p0eUBg/
        https/media.tenor.com/VAgfPZcM340AAAPo/bof-i-dont-mind.mp4"""


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
