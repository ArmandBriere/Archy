import flask
import functions_framework
from bs4 import BeautifulSoup
import requests
from datetime import datetime

def examensScraper(course, semester, year):
    url_link = f"https://etudier.uqam.ca/wshoraire/cours/{course}/{year}{semester}/7316"
    try:
        result = requests.get(url_link).text
        soup = BeautifulSoup(result, "html.parser")
        name_box = soup.find(lambda tag: tag.name == "li" and "Examens" in tag.text)
        name = name_box.text.strip()  # strip() is used to remove starting and trailing
    except:
        return None

    if name is None:
        return None

    name = name.replace("Examens: ", "")
    dates = name.split("et")
    return dates

def getSemester():
    from datetime import date
    currentYear = str(date.today().year)
    winter = ["01-01-" + currentYear, "04-30-" + currentYear]
    summer = ["01-05-" + currentYear, "08-30-" + currentYear]
    fall = ["01-09-" + currentYear, "12-21-" + currentYear]

    d = date.today()
    currentDate = datetime(d.year, d.month, d.day)

    if datetime.strptime(winter[0], '%m-%d-%Y') <= currentDate <= datetime.strptime(winter[1], '%m-%d-%Y'):
        return 2
    elif datetime.strptime(summer[0], '%m-%d-%Y') <= currentDate <= datetime.strptime(summer[1], '%m-%d-%Y'):
        return 3
    elif datetime.strptime(fall[0], '%m-%d-%Y') <= currentDate <= datetime.strptime(fall[1], '%m-%d-%Y'):
        return 1
    else:
        return 0

def getChannelName(request):
    request_json = request.get_json(silent=True)
    channelName = request_json.get("server_name", None)
    if channelName.include("#"):
        channelName.replace("#", "")
    return channelName.lower()

@functions_framework.http
def infoCours(request):
    """This is a template function that show how to send back message."""


    request_json: Optional[Any] = request.get_json(silent=True)

    if request_json:
        user_id = request_json.get("user_id", None)
        if user_id:
            return f"Hello Monsieur <@{user_id}>!", 200

    return "Hello Monsieur!", 200

