import json
import os
from typing import Optional, Tuple

import functions_framework
import requests
from flask.wrappers import Request

MEME_FILE = "memes.json"

NO_EMOJI = "https://cdn.discordapp.com/emojis/823403768448155648.webp"
USAGE_GUIDE = "Usage: !meme <Meme name> <Top text> <Bottom text (Optional)>"
UNSUPORTED_MEME = "Meme not in supported list."


@functions_framework.http
def meme(request: Request) -> Tuple[str, int]:
    """Return url to generated meme."""

    request_json: Optional[dict] = request.get_json(silent=True)

    with open(MEME_FILE, "r", encoding="utf-8") as meme_file:
        memes: dict = json.load(meme_file)

    if request_json:
        params: list = request_json.get("params", [""])

        if len(params) != 2 and len(params) != 3:
            return USAGE_GUIDE, 200
        if params[0] not in memes:
            return UNSUPORTED_MEME, 200

        request_body: dict = {
            "template_id": memes.get(params[0]),
            "username": os.environ["IMGFLIP_API_USERNAME"],
            "password": os.environ["IMGFLIP_API_PASSWORD"],
            "text0": params[1],
        }
        if len(params) == 3:
            request_body["text1"] = params[2]

        response: requests.Response = requests.post("https://api.imgflip.com/caption_image", data=request_body)
        if not response.ok:
            return NO_EMOJI, 200
        response_json: dict = response.json()

        if not response_json.get("success"):
            return NO_EMOJI, 200

        data: dict | None = response_json.get("data")
        if data:
            return str(data.get("url")), 200

    return USAGE_GUIDE, 200
