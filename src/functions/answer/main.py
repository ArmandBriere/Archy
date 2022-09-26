import random
from typing import Tuple

import functions_framework

POSSIBLE_ANSWERS = [
    "It is certain",
    "Reply hazy, try again",
    "Don't count on it",
    "It is decidedly so",
    "Ask again later",
    "My reply is no",
    "Without a doubt",
    "Better not tell you now",
    "My sources say no",
    "Yes definitely",
    "Cannot predict now",
    "Outlook not so good",
    "You may rely on it",
    "Concentrate and ask again",
    "Very doubtful",
    "As I see it, yes",
    "Most likely",
    "Outlook good",
    "Yes",
    "Signs point to yes",
]


@functions_framework.http
def answer(_request) -> Tuple[str, int]:
    """This is a function that returns a random answer from a predefined list based on 8ball."""

    return random.choice(POSSIBLE_ANSWERS), 200
