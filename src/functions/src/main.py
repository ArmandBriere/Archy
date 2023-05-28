from typing import Tuple

import flask
import functions_framework

SOURCE_CODE_URL = "https://github.com/ArmandBriere/Archy"


@functions_framework.http
def sourcecode(_request: flask.Request) -> Tuple[str, int]:
    """Function that returns the github url to my code"""

    return SOURCE_CODE_URL, 200
