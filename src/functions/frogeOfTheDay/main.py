# pylint: disable=C0103,E1136

import base64
import json
import random
from email.generator import Generator
from io import BytesIO
from typing import Any, List, Tuple

import requests
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


def generate_froge_of_the_day() -> str:
    """Generate the froge of the day with quote."""

    random_image = f"{random.randint(1, 54):04.0f}.jpg"
    random_text = ""
    while len(random_text) > 120 or len(random_text) < 10:
        random_text_request = requests.get("https://programming-quotes-api.herokuapp.com/quotes/random")
        random_text = json.loads(random_text_request.content.decode("utf-8"))["en"].replace("’", "'")

    print(f"Quote of the day is: {random_text}")

    froge_of_the_day = auto_scale_text_over_image(Image.open(f"{IMAGE_FOLDER}{random_image}"), text=random_text)

    buffered = BytesIO()
    froge_of_the_day.save(buffered, format="JPEG")

    return base64.b64encode(buffered.getvalue()).decode("UTF-8")


def publish_message_discord(channels: List[str], image_str: str = "") -> None:
    """Publish image to channel_message_discord."""

    if len(image_str) == 0:
        print("Exit: No image provided")
        return

    project_id = "archy-f06ed"
    topic_id = "channel_message_discord"
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
