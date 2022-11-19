import dateparser, datetime, json

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
        self.done = 0
        if collabs != None :
            self.collabs = list(collab for collab in collabs)
        else : 
            self.collabs = []
            
    def update(self, title=None, date=None, description=None, collabs=None,done=None):
        if date:
            self.date = date
        if title:
            self.title =title
        if description:
            self.description = description
        if collabs:
            self.collabs = list(collab for collab in collabs)
        if done:
            self.done = 1


    
    def toPrint(self) :
        print("Title : ",self.title,"\nDue Date : ",self.date,"\nDescription : ",self.description,"\nCreated by : ",self.who," @ ",self.whenCreated(),"\nCollaborateurs : ",' '.join(str(x) for x in self.collabs))
    
    def toJson(self) :
        obj = {
            "Title" : self.title,
            "Creator" : self.who,
            "DueDate" : self.date,
            "Collabs" : self.collabs,
            "Description" : self.description,
            "CreateDate" : self.createDate,
            "Done" : self.done
        }
        return obj
    
    def __repr__(self):
        return """
        # {0}
        ###Created on {1}
        ###By user : {2}
        {3}""".format(self.what, self.when, self.who, self.what)

    def whenCreated(self):
        return self.createDate


def readTitle(text) :
    title = ""
    titleIndex = [0]
    for i in range(len(text.split())) :
        if ('%' in text.split()[i]) or ('"' in text.split()[i]) or (i == len(text.split())) :
            titleIndex.append(i)
            
    if len(titleIndex) >= 2 :
        for index in range(titleIndex[0],titleIndex[1]) :
            title+=text.split()[index]+' '
        return title[0:-1]
    else :
        return None
    
    
def readDesc(text) :
    desc = ""
    descIndex = []
    for i in range(len(text)) :
        if text[i] == '"' :
            descIndex.append(i)
    if len(descIndex) == 2 :
        
       
        desc = text[descIndex[0]:descIndex[1]]
        return desc[1:]
    else :
        return None
            
        
def readDate(text) :
    date = ""
    dateIndex = []
    for i in range(len(text)) :
        if text[i] == '%':
            dateIndex.append(i)
        if text[i] == ('@' or '"') or (i==len(text)) :
            dateIndex.append(i)
    if len(dateIndex) >= 2 :
        date = text[dateIndex[0]:dateIndex[1]]
        return date[1:]
    else :
        return None
    


def createTodo(text, mentions, user_id):
    title = ""
    for i in range(len(text)):
        if i+1 == len(text) and "%" not in text[i]:
            raise ValueError # Pas de date ou quoi que ce soit après le titre
        if "%" in text[i]:
            text = text[i:]
            break
        title += text[i] + " "
    if "%" not in text[0]:
        raise ValueError # pas d'indicateur de date dans les arguments
    date_string= ""
    for i in range(len(text)):
        if '"' in text[i]:
            text = text[i:]
            break
        date_string += text[i] + " "
    date = dateparser.parse(date_string.strip("%"))
    if date is None:
        raise ValueError # la date n'est pas correcte

    if '"' not in str(text):
        return str(Todo(user_id, title=title, date=date, collabs=mentions))
    else:
        description = text[0].strip('"')
        if len(text)>0:
            text = text[1:]
        for i in range(len(text)):
            if '"' in text[i]:
                description += text.strip('"')
                break
            description += text[i] + " "
        return str(Todo(user_id, title=title, date=date, description=description, collabs=mentions))

def newCreate(text,mentions,user_id) :
    pass
        


def getTodo(todoId, title):


def getAllTodo(user_id):
    pass

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
        try:
            if text[0].lower() == "create":
                return str(createTodo(text[1:], mentions, user_id)), 200
            elif text[0].lower() == "update":
                return str(updateTodo(text[1:], mentions, user_id)), 200
            elif text[0].lower() == "list":
                return str(listTodos(text[1:], mentions, user_id)), 200
            else:
                return USAGE, 200
        except:
            return USAGE, 200







