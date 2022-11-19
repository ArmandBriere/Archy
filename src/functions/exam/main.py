from datetime import date, datetime
from typing import Any, Optional

import flask
import functions_framework
import requests
from bs4 import BeautifulSoup


def examens_scraper(course: str, semester: str) -> list[str]:
    """Function that scrapes schedule website for exam dates"""

    current_year = str(date.today().year)
    url_link = f"https://etudier.uqam.ca/wshoraire/cours/{course}/{current_year}{semester}/7316"
    try:
        result = requests.get(url_link).text
        soup = BeautifulSoup(result, "html.parser")
        name_box = soup.find(lambda tag: tag.name == "li" and "Examens" in tag.text)
        name = name_box.text.strip()  # strip() is used to remove starting and trailing
    except AttributeError:
        return []

    if name is None:
        return []
    name = name.replace("Examens: ", "")
    dates = name.split("et")
    return dates


def get_semester() -> str:
    """Function that returns the current semester"""

    current_year = str(date.today().year)
    winter = ["01-01-" + current_year, "04-30-" + current_year]
    summer = ["01-05-" + current_year, "08-30-" + current_year]
    fall = ["01-09-" + current_year, "12-21-" + current_year]

    date_today = date.today()
    current_date = datetime(date_today.year, date_today.month, date_today.day)

    if datetime.strptime(winter[0], "%m-%d-%Y") <= current_date <= datetime.strptime(winter[1], "%m-%d-%Y"):
        return "1"
    if datetime.strptime(summer[0], "%m-%d-%Y") <= current_date <= datetime.strptime(summer[1], "%m-%d-%Y"):
        return "2"
    if datetime.strptime(fall[0], "%m-%d-%Y") <= current_date <= datetime.strptime(fall[1], "%m-%d-%Y"):
        return "3"
    return "0"


def get_channel_name(request_json: Optional[Any]) -> str:
    """Function that returns the current channel name"""

    channel_name: str = request_json.get("channel_name", None)
    if not channel_name:
        return ""
    return channel_name.lower()


def display_exams(course: str, semester: str) -> str:
    """Function that returns message to be displayed to the channel"""

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
def exam(request: flask.Request) -> str:
    """Function that displays exam info from current semester for a channel"""

    request_json: Optional[Any] = request.get_json(silent=True)

    if request_json:
        semester = get_semester()
        course = get_channel_name(request_json)
        message = display_exams(course, semester)
        return message
    return "Je n'ai rien trouvé"