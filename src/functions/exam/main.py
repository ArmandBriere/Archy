from datetime import datetime
from datetime import date
from typing import Any, Optional
from bs4 import BeautifulSoup
import functions_framework
import requests

def examens_scraper(course, semester):
    current_year = str(date.today().year)
    url_link = f"https://etudier.uqam.ca/wshoraire/cours/{course}/{current_year}{semester}/7316"
    try:
        result = requests.get(url_link).text
        soup = BeautifulSoup(result, "html.parser")
        name_box = soup.find(lambda tag: tag.name == "li" and "Examens" in tag.text)
        name = name_box.text.strip()  # strip() is used to remove starting and trailing
    except AttributeError:
        return None

    if name is None:
        return None

    name = name.replace("Examens: ", "")
    dates = name.split("et")
    return dates

def get_semester():
    current_year = str(date.today().year)
    winter = ["01-01-" + current_year, "04-30-" + current_year]
    summer = ["01-05-" + current_year, "08-30-" + current_year]
    fall = ["01-09-" + current_year, "12-21-" + current_year]

    date_today = date.today()
    current_date = datetime(date_today.year, date_today.month, date_today.day)

    if datetime.strptime(winter[0], "m-%d-%Y") <= current_date <= datetime.strptime(winter[1], "%m-%d-%Y"):
        return 2
    if datetime.strptime(summer[0], "%m-%d-%Y") <= current_date <= datetime.strptime(summer[1], "%m-%d-%Y"):
        return 3
    if datetime.strptime(fall[0], "%m-%d-%Y") <= current_date <= datetime.strptime(fall[1], "%m-%d-%Y"):
        return 1
    return 0

def get_channel_name(request_json):
    channel_name = request_json.get("channel_name", None)
    if channel_name.include("#"):
        channel_name.replace("#", "")
    if not channel_name:
        return ""
    return channel_name.lower()

def display_exams(course, semester):
    exams = examens_scraper(course, semester)
    message = ""

    if not exams:
        return "Je n'ai rien trouvé"
    if len(exams) == 1:
        message += "Exam finale: " + exams[0] + "\n"
    else:
        message += "Vos exams: \n"
        message += "Intra: " + exams[0] + "\n"
        message += "Finale: " + exams[1] + "\n"
    return message

@functions_framework.http
def exam(request):
    """Function to return exam info for a channel"""

    request_json: Optional[Any] = request.get_json(silent=True)

    if request_json:
        semester = get_semester()
        course = get_channel_name(request_json)
        message = display_exams(course, semester)
        return message
    return "Je n'ai rien trouvé"
