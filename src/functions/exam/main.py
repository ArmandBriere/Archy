from datetime import date, datetime
from typing import Any, Optional

import flask
import functions_framework
import requests
from bs4 import BeautifulSoup

SEMESTER_ID = {
    "not_found": "0",
    "winter": "1",
    "summer": "2",
    "fall": "3",
}
DATE_TIME_FORMAT = "%m-%d-%Y"


def examens_scraper(course: str, semester: str) -> list[str]:
    """Function that scrapes schedule website for exam dates"""

    current_year = str(date.today().year)
    url_link = f"https://etudier.uqam.ca/wshoraire/cours/{course}/{current_year}{semester}/7316"
    try:
        result = requests.get(url_link, timeout=5).text
        soup = BeautifulSoup(result, "html.parser")
        name_box = soup.find(lambda tag: tag.name == "li" and "Examens" in tag.text)
        name = name_box.text.strip()
    except AttributeError:
        return []
    if name is None:
        return []
    return name.replace("Examens: ", "").split("et")


def get_semester() -> str:
    """Function that returns the current semester"""

    current_year = str(date.today().year)
    fall_start, fall_end = f"01-09-{current_year}", f"12-21-{current_year}"
    winter_start, winter_end = f"01-01-{current_year}", f"04-30-{current_year}"
    summer_start, summer_end = f"01-05-{current_year}", f"08-30-{current_year}"
    date_today = date.today()
    current_date = datetime(date_today.year, date_today.month, date_today.day)

    if (
        datetime.strptime(winter_start, DATE_TIME_FORMAT)
        <= current_date
        <= datetime.strptime(winter_end, DATE_TIME_FORMAT)
    ):
        return SEMESTER_ID["winter"]
    if (
        datetime.strptime(summer_start, DATE_TIME_FORMAT)
        <= current_date
        <= datetime.strptime(summer_end, DATE_TIME_FORMAT)
    ):
        return SEMESTER_ID["summer"]
    if datetime.strptime(fall_start, DATE_TIME_FORMAT) <= current_date <= datetime.strptime(fall_end, DATE_TIME_FORMAT):
        return SEMESTER_ID["fall"]
    return SEMESTER_ID["not_found"]


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
        return "Sorry, this class doesn't have a shared exam"
    if len(exams) == 1:
        message += f"Final: {exams[0]}\n"
    else:
        message += "Your exams: \n"
        message += f"Intra: {exams[0]}\n"
        message += f"Final: {exams[1]}\n"
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
    return "Sorry, I didn't find anything"
