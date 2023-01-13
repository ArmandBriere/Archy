# pylint: disable=C0103,E1136

import base64
import json
import os
import random
from email.generator import Generator
from io import BytesIO
from typing import Any, List, Tuple

from google.cloud.firestore_v1.client import Client
from google.cloud.firestore_v1.document import DocumentReference, DocumentSnapshot
from google.cloud.pubsub_v1 import PublisherClient
from google.cloud.pubsub_v1.publisher.futures import Future
from PIL import Image, ImageDraw, ImageFont

IMAGE_FOLDER = "img/"


def auto_scale_text_over_image(
    img: Image,
    text: str,
    shadow: Tuple[int, int] = (2, 2),
    shadow_color: Tuple[int, int, int] = (0, 0, 0),
) -> Image:
    """Resize image and add text over it."""

    width = 500
    img_width: int = img.size[0]
    img_height: int = img.size[1]
    ratio: float = width / float(img_width)

    resized_h: int = int((float(img_height) * float(ratio)))
    resized_img: Image = img.resize((width, resized_h))

    x_max = (resized_img.size[0] * 10) // 100

    font_path: str = "./SourceHanSansSC-Regular.otf"
    font: ImageFont = ImageFont.truetype(font=font_path, size=25)
    lines: int = text_wrap(text, font, resized_img.size[0] - x_max)
    line_height: int = font.getsize("hg")[1]

    y_max: float = (resized_img.size[1] * 80) // 100 - len(lines) * line_height

    draw: ImageDraw = ImageDraw.Draw(resized_img)

    x = x_max
    y = y_max

    for line in lines:
        draw.text((x + shadow[0], y + shadow[1]), line, font=font, fill=shadow_color)
        draw.text((x, y), line, fill="white", font=font)

        y += line_height

    return resized_img


def text_wrap(text: str, font: ImageFont, max_width: int) -> List[str]:
    """Wrap text based on width and font size."""

    lines: List[str] = []

    if font.getsize(text)[0] <= max_width:
        lines.append(text)
    else:
        words: List[str] = text.split(" ")
        i = 0
        while i < len(words):
            line = ""
            while i < len(words) and font.getsize(line + words[i])[0] <= max_width:
                line = line + words[i] + " "
                i += 1
            if not line:
                line = words[i]
                i += 1
            lines.append(line)

    return lines


def get_all_channels() -> List[str]:
    """Return the channels id from Firestore"""

    channels: List[str] = []

    database: Client = Client(project="archy-f06ed")
    servers: Generator[DocumentSnapshot, Any, None] = database.collection("servers").list_documents()

    for server in servers:
        print(f"ServerId: {server.id}")
        server: DocumentReference
        doc_ref: DocumentReference = (
            database.collection("servers").document(server.id).collection("channels").document("froge_of_the_day")
        )
        doc: DocumentSnapshot = doc_ref.get()
        if doc.exists and doc.get("active"):
            print(f"Will publish froge to this server: {server.id}")
            channels.append(doc.get("channel_id"))
        else:
            print(f"Will NOT publish froge to this server: {server.id}")

    return channels


def get_quote() -> dict:
    """Return a random quote."""
    quotes = [
        {"quote": "All my homies hate javascript", "author": "zactrixo#8903"},
        {"quote": "Throw sh*t at the wall until it sticks", "author": "zactrixo#8903"},
        {"quote": "BlueJ is actually NOT underrated! It's really not good...", "author": "Jay Cee#5430"},
        {"quote": "Rust is love, Rust is life.", "author": "FireLexFtw#8683"},
        {"quote": "C# is like java, but its better", "author": "zactrixo#8903"},
        {"quote": "Fais ton TP", "author": "Hannibal119#3744"},
        {"quote": "Code it", "author": "Hannibal119#3744"},
        {"quote": "Git gud", "author": "Hannibal119#3744"},
        {"quote": "damn archy is down again", "author": "FireLexFtw#8683"},
        {"quote": "rakabicyk katredmi ?", "author": "moonscrub#5366"},
        {"quote": "entRE Quote PleaSe sinON Je PreNDs pas LeS meSsagES", "author": "FireLexFtw#8683"},
        {"quote": "My love for you is stronger than an infinite loop", "author": "coder4life#4678"},
        {"quote": "je suis juste ici pour les bidoux", "author": "arth-e#0399"},
        {"quote": "..... how did everything broke", "author": "Grisamah#2143"},
        {"quote": "j'comprends pas les pointeurs", "author": "Grisamah#2143"},
        {"quote": "why are we using javasript again?", "author": "Grisamah#2143"},
        {
            "quote": "À l'ÉTS ya assez de prises pour tout le monde dans les salles de cours!",
            "author": "moonscrub#5366",
        },
        {
            "quote": "Si vous avez besoin d'aide en INF3105, regardez les capsules d'Hannibal",
            "author": "moonscrub#5366",
        },
        {"quote": "Froge Jesus will save us all! Amen!", "author": "moonscrub#5366"},
        {"quote": "Alex a en fait un grand cœur!", "author": "moonscrub#5366"},
        {"quote": "You all need Froge Jesus!", "author": "moonscrub#5366"},
        {"quote": "Tokébakicitte", "author": "moonscrub#5366"},
        {"quote": "Faites vos noeuds en 8 comme il faut avant de faire la voie!", "author": "moonscrub#5366"},
        {"quote": "Oubliez pas de regarder si ya un tour de friction avant d'assurer!", "author": "moonscrub#5366"},
        {"quote": "Si j'peux faire une injection sql sur ton app, tu vas avoir un beau 0!", "author": "moonscrub#5366"},
        {"quote": "Haskell is actually underrated!", "author": "moonscrub#5366"},
        {"quote": "Come contribute to my code and add some new features!", "author": "moonscrub#5366"},
        {"quote": "Come check my source code on github", "author": "moonscrub#5366"},
        {
            "quote": "Il semble que les services informatiques de l'UQÀM ont besoin de financement supplémentaire",
            "author": "moonscrub#5366",
        },
        {"quote": "Http/1.1 Service Unavailable - Portail UQÀM Janvier 2023", "author": "Yannick#5937"},
        {"quote": "Shrodinger's portail étudiant", "author": "opdelta#1665"},
        {"quote": "TikTok beurk, Logiciel espion pour le gouv chinois!", "author": "opdelta#1665"},
        {"quote": "TikTok beurk, Logiciel espion pour le gouv chinois!", "author": "moonscrub#5366"},
        {"quote": "TikTok beurk, Logiciel espion pour le gouv chinois!", "author": "Hannibal119#3744"},
        {"quote": "Je vous conseille de ne pas utiliser TikTok.", "author": "moonscrub#5366"},
        {
            "quote": "With C it doesn't work and you don't know why. With python it works but you don't know why!"
            + " So C is better.",
            "author": "moonscrub#5366",
        },
        {
            "quote": "Programming is like sex: One mistake and you have to support it for the rest of your life.",
            "author": "arth-e#0399",
        },
        {"quote": "Fun fact: Archy is the greatest discord bot in the world", "author": "moonscrub#5366"},
        {
            "quote": "Ouais ben tsé, j'expérimentais la semaine passée sur un microprocesseur à cycle unique x86...",
            "author": "moonscrub#5366",
        },
        {"quote": "Le serveur du bot serverless est down", "author": "Yannick#5937"},
        {"quote": "?.... it works", "author": "Grisamah#2143"},
        {
            "quote": "There are two hard things in computer science: cache invalidation, naming things,"
            + " and off-by-one errors.",
            "author": "opdelta#1665",
        },
    ]

    return random.choice(quotes)


def generate_froge_of_the_day() -> str:
    """Generate the froge of the day with quote."""

    random_image = f"{random.randint(1, 54):04.0f}.jpg"
    quote = get_quote()

    print(f"Quote of the day is: {quote['quote']}")

    froge_of_the_day = auto_scale_text_over_image(Image.open(f"{IMAGE_FOLDER}{random_image}"), text=quote["quote"])

    buffered = BytesIO()
    froge_of_the_day.save(buffered, format="JPEG")

    return base64.b64encode(buffered.getvalue()).decode("UTF-8")


def publish_message_discord(channels: List[str], image_str: str = "") -> None:
    """Publish image to channel_message_discord."""

    if len(image_str) == 0:
        print("Exit: No image provided")
        return

    project_id = "archy-f06ed"

    environment = os.getenv("K_SERVICE").split("_")[0]
    topic_id = f"{environment}_channel_message_discord"

    publisher = PublisherClient()
    topic_path: str = publisher.topic_path(project_id, topic_id)

    message = "Here is the Froge of the Day!"

    for channel_id in channels:
        data = {"channel_id": channel_id, "message": message, "image": image_str}
        encoded_data = json.dumps(data, indent=2).encode("utf-8")

        print("Publishing data")
        future: Future = publisher.publish(topic_path, encoded_data)

        print(f"Message id: {future.result()}")
        print(f"Published message to {topic_path}.")


def publish_froge_of_the_day(_event: Any, _context: Any) -> None:
    print("Start")

    channels = get_all_channels()
    if len(channels) == 0:
        print("Exit: No channel found")
        return

    base64_image = generate_froge_of_the_day()

    publish_message_discord(channels, base64_image)
