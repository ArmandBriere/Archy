import functions_framework

DEFAULT_GIF = "https://tenor.com/view/the-rock-hmmm-gif-21574594"
UNKNOWN_GIF = "https://tenor.com/view/bof-i-dont-mind-i-dont-understand-why-jean-dujardin-oss117-gif-20383956"

gifs = {
    "doubt": "https://tenor.com/view/doubt-press-x-la-noire-meme-x-button-gif-19259237",
    "confused": "https://tenor.com/view/confusion-chicken-gif-11299790",
}


@functions_framework.http
def gif(request):
    """HTTP Cloud Function."""
    request_json = request.get_json(silent=True)
    if request_json:
        params = request_json.get("params", [""])
        name_gif = params[0].lower()
        if name_gif in gifs:
            return gifs[name_gif]
        return UNKNOWN_GIF
    return DEFAULT_GIF
