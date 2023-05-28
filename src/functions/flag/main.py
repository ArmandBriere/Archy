from typing import Tuple

import flask
import functions_framework


@functions_framework.http
def flag(_request: flask.Request) -> Tuple[str, int]:
    """This function returns a flag emoji..."""

    the_flag = ":triangular_flag_on_post:"

    return the_flag, 200
