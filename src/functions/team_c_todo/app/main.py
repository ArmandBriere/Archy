import dateparser, datetime

from typing import Any, Optional, Tuple

import flask
import functions_framework

USAGE = """
# Todo
## Usage :
/todo <title> %<date> @<collaborateur> "<description>"
/todo update [title or date or collabs or description] <value>
Enter a new value for the aspect you are modifying instead of <value>, collabs *need* to start with "@".
"""


class Todo:
    def __init__(self, who, date=None, title=None, associates=None, description=None):
        self.createDate = datetime.datetime.now()
        self.who = who
        self.date = date
        self.title = title
        self.description = description
        self.associates = associates

    def update(self, date=None, title=None, description=None, collabs=[]):
        if date:
            self.date = date
        if title:
            self.title =title
        if description:
            self.description = description
        if collabs:
            self.collabs = collabs

    def __repr__(self):
        return """
        ### {0}
        Created on {1}
        To do before : {2}
        By user : {3}
        Collabs : {4}
        """.format(self.title, self.createDate, self.date, self.who, str(self.collabs))

    def whenCreated(self):
        return self.createDate

@functions_framework.http
def todo(request: flask.Request) -> Tuple[str, int]:
    request_json: Optional[Any] = request.get_json(silent=True)
    if request_json:
        user_id = request_json["user_id"]
        text = request_json["content"]
        if not text:  # !todo
            return USAGE, 200
        else:
            date = dateparser.parse(text.split("%")[1][2:].split("@")[0].split('"')[0])
            title = text.split("%")[0]
            collabs = []
            for i in text.split('"')[0].split(" "):
                if i[0] == "@":
                    collabs.append(i)

            new_todo = Todo(user_id,)

"""
- Comment acceder a l'entrée d'un utilisateur
- Comment sont passés les entrées (avec ou sans arg[0] ?)
- Comment faire tourner un while qui capture l'entrée

"""
