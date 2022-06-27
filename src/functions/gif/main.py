import json
import os

import functions_framework
import requests

DEFAULT_GIF = "https://tenor.com/view/frog-multiply-gif-25342428"
UNKNOWN_GIF = "https://tenor.com/view/bof-i-dont-mind-i-dont-understand-why-jean-dujardin-oss117-gif-20383956"

gifs = {
    "doubt": "https://tenor.com/view/doubt-press-x-la-noire-meme-x-button-gif-19259237",
    "confused": "https://tenor.com/view/confusion-chicken-gif-11299790",
}


@functions_framework.http
def gif(request):
    """Return the requested gif or the first found with the tenor API."""
    request_json: Optional[Any] = request.get_json(silent=True)
    if request_json:
        params = request_json.get("params", [""])
        api_key = os.environ["TENOR_API_TOKEN"]

        if len(params) == 0:
            return DEFAULT_GIF
        if params[0].lower() in gifs:
            return gifs[params[0]]
        api_request = requests.get(
            f"https://tenor.googleapis.com/v2/search?q={params[0].lower()}&key={api_key}&client_key=Archy&limit=1"
        )

        return get_gif_from_api(api_request.status_code, api_request.content)
    return DEFAULT_GIF


def get_gif_from_api(api_request_status, api_json):
    """Function that deals with the api request result"""
    if api_request_status == 200:
        top_gif = json.loads(api_json)
        try:
            url_gif = top_gif["results"][0]["media_formats"]["gif"]["url"]
            return url_gif
        except (IndentationError, KeyError):
            return "https://tenor.com/view/im-dead-vanilla-patay-na-ako-dead-nako-patay-ako-gif-22020482"
    return UNKNOWN_GIF
