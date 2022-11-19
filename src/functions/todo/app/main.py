import dateparser, datetime

from typing import Any, Optional, Tuple

import flask
import functions_framework


class Todo:
    def __init__(self, who, date=None, title=None, associates=None, description=None):
        self.createDate = datetime.datetime.now()
        self.who = who
        self.date = date
        self.title = title
        self.description = description
        self.associates = associates

    def update(self, date=None, title=None, description=None):
        if date:
            self.date = date
        if title:
            self.title =title
        if description:
            self.description = description



    def __repr__(self):
        return """
        # {0}
        ###Created on {1}
        ###By user : {2}
        {3}""".format(self.what, self.when, self.who, self.what)

    def whenCreated(self):
        return self.createDate

@functions_framework.http
def todo(request: flask.Request) -> Tuple[str, int]:
    request_json: Optional[Any] = request.get_json(silent=True)
    return str(request_json), 200

