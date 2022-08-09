from html2image import Html2Image
from jinja2 import Template

hti = Html2Image()
hti.browser_executable = "/usr/bin/google-chrome-stable"

with open("../templates/level.html") as file_:
    tm = Template(file_.read())
    hti.screenshot(
        html_str=tm.render(
            username="Hannibal119",
            avatar_url="https://cdn.discordapp.com/avatars/135048445097410560/cf784bf15d1575d1feee5e35692dd3dc.webp",
            rank=1,
            level=55,
            percent=50,
        ),
        save_as="hannibal119.png",
        size=(1680, 720),
    )

from flask import Flask, render_template

app = Flask(__name__, template_folder="../templates")


@app.route("/")
def home():
    return render_template(
        "level.html",
        username="Hannibal119",
        avatar_url="https://cdn.discordapp.com/avatars/135048445097410560/cf784bf15d1575d1feee5e35692dd3dc.webp",
        rank=1,
        level=55,
        percent=25,
    )


if __name__ == "__main__":
    app.run(port=4201)
