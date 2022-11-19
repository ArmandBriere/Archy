import flask
import functions_framework
from bs4 import BeautifulSoup
import requests
from datetime import datetime
from datetime import date

def examensScraper(course, semester):
    currentYear = str(date.today().year)
    url_link = f"https://etudier.uqam.ca/wshoraire/cours/{course}/{currentYear}{semester}/7316"
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

def displayExams(course, semester):
    exams = examensScraper(course, semester)

    if not exams:
        return "Je n'ai rien trouvé"
    else:
        message = "Vos exams: \n"
        message += "Intra: " + exams[0] + "\n"
        message += "Finale: " + exams[1] + "\n"


@functions_framework.http
def examen(request):
    """Function to return exam info for a channel"""

    request_json: Optional[Any] = request.get_json(silent=True)

    if request_json:
        request_json: Optional[Any] = request.get_json(silent=True)

        semester = getSemester()
        course = getChannelName(request)

        message = displayExams(course, semester)

        return message
    else:
        return "Je n'ai rien trouvé"
