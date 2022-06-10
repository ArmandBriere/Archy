import json
import os

import functions_framework
import requests
from dotenv import load_dotenv

# need nev file with tenor api key
load_dotenv()


DEFAULT_GIF = "https://tenor.com/view/frog-multiply-gif-25342428"
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
        api_key = os.getenv("API_TOKEN")
        if len(params) == 0:
            return DEFAULT_GIF
        if params[0].lower() in gifs:
            return gifs[params[0]]
        api_request = requests.get(f"https://g.tenor.com/v1/search?q={params[0].lower()}&key={api_key}&limit=1")
        if api_request.status_code == 200:
            top_1gifs = json.loads(api_request.content)
            url_gif = top_1gifs["results"][0]["media"][0]["gif"]["url"]
            return url_gif
        return UNKNOWN_GIF
    return DEFAULT_GIF
