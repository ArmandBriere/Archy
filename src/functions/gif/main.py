import functions_framework
from typing import Any, Optional

DEFAULT_GIF = "https://tenor.com/view/frog-multiply-gif-25342428"
UNKNOWN_GIF = "https://tenor.com/view/bof-i-dont-mind-i-dont-understand-why-jean-dujardin-oss117-gif-20383956"

gifs = {
    "doubt": "https://tenor.com/view/doubt-press-x-la-noire-meme-x-button-gif-19259237",
    "confused": "https://tenor.com/view/confusion-chicken-gif-11299790",
}


@functions_framework.http
def gif(request):
    """HTTP Cloud Function."""

    request_json: Optional[Any] = request.get_json(silent=True)
    if request_json:
        params = request_json.get("params", [""])
        if len(params) == 0:
            return DEFAULT_GIF
        if params[0].lower() in gifs:
            return gifs[params[0]]
        return UNKNOWN_GIF
    return DEFAULT_GIF
