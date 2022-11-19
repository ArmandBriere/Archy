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
    def __init__(self, who, date=None, title=None, collabs=None, description=None):
        self.createDate = datetime.datetime.now()
        self.who = who
        self.date = date
        self.title = title
        self.description = description
        self.collabs = collabs

    def update(self, date=None, title=None, description=None, collabs=None):
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


def createTodo(text, mentions, user_id):
    title = ""
    for i in range(len(text)):
        title += text[i]+" "
        if "%" in text[i]:
            text = text[i:]
            break
    if


def updateTodo(text, mentions, user_id):
    pass


def deleteTodo(text, mentions, user_id):
    pass


def listTodos(text, mentions, user_id):
    pass


@functions_framework.http
def todo(request: flask.Request) -> Tuple[str, int]:
    request_json: Optional[Any] = request.get_json(silent=True)
    if request_json:
        user_id = request_json["user_id"]
        text = request_json["params"]
        mentions = request_json["mentions"]
        if not text:  # !todo
            return USAGE, 200
        elif text[0].lower() == "create":
            return createTodo(text[1:], mentions, user_id)
        elif text[0].lower() == "update":
            return updateTodo(text[1:], mentions, user_id)
        elif text[0].lower() == "list":
            return listTodos(text[1:], mentions, user_id)
        else:
            return USAGE, 200






