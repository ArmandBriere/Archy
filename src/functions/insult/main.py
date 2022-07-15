import json
import re
from typing import Any, Optional, Tuple

import flask
import functions_framework
import requests

REPLACE_USER_NAME = "!_A_USER_NAME_!"
BASE_INSULT = "So bad even Archy can't stand you, jk <3"


@functions_framework.http
def insult(request: flask.Request) -> Tuple[str, int]:
    """Return a random insult to the tagged user or the author"""

    request_json: Optional[Any] = request.get_json(silent=True)

    if request_json:
        mentions: list = request_json.get("mentions", None)

        if mentions is None or len(mentions) == 0:
            response: requests.Response = requests.get("https://insult.mattbas.org/api/en/insult.json")
            return get_insult(response), 200

        if len(mentions) == 1:
            response: requests.Response = requests.get(
                f"https://insult.mattbas.org/api/en/insult.json?who={REPLACE_USER_NAME}"
            )
            return add_tag_users(get_insult(response), mentions), 200

        if len(mentions) > 1:
            response: requests.Response = requests.get(
                f"https://insult.mattbas.org/api/en/insult.json?who={REPLACE_USER_NAME}&plural"
            )
            return add_tag_users(get_insult(response), mentions), 200

    return BASE_INSULT, 200


def get_insult(response: requests.Response) -> str:
    """Function that deals with the api request result"""

    if response.status_code == 200:
        insult_res = json.loads(response.content)

        try:
            return insult_res["insult"]
        except KeyError:
            return BASE_INSULT

    return "Is that an Archy reference?"


def add_tag_users(an_insult: str, mentions: list[str]) -> str:
    """Function that adds the mentions to the messages"""

    people_tag = ""

    if len(mentions) == 1:
        people_tag = f"<@{mentions[0]}>"

    if len(mentions) > 1:
        people_tag = ", ".join([f"<@{mention}>" for mention in mentions])

    final_insult = re.sub(REPLACE_USER_NAME, people_tag, an_insult)

    return final_insult
