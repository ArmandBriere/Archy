# pylint: disable=C0103

import base64
import json
import random
from io import BytesIO

import requests
from google.cloud import pubsub_v1
from PIL import Image, ImageDraw, ImageFont

IMAGE_FOLDER = "img/"


def auto_scale_text_over_image(
    img,
    text,
    shadow=(2, 2),
    shadow_color=(0, 0, 0),
):
    # Resize the image
    width = 500
    img_w = img.size[0]
    img_h = img.size[1]
    wpercent = width / float(img_w)
    hsize = int((float(img_h) * float(wpercent)))
    rmg = img.resize((width, hsize))

    # Set x boundry
    x_max = (rmg.size[0] * 10) // 100

    font_path = "./SourceHanSansSC-Regular.otf"
    font = ImageFont.truetype(font=font_path, size=25)
    lines = text_wrap(text, font, rmg.size[0] - x_max)
    line_height = font.getsize("hg")[1]

    # Set y boundry
    y_max = (rmg.size[1] * 80) // 100
    y_max -= len(lines) * line_height

    draw = ImageDraw.Draw(rmg)
    color = "white"
    x = x_max
    y = y_max
    for line in lines:
        draw.text((x + shadow[0], y + shadow[1]), line, font=font, fill=shadow_color)
        draw.text((x, y), line, fill=color, font=font)

        y = y + line_height  # update y-axis for new line

    return rmg


def text_wrap(text, font, max_width):
    lines = []

    # If the text width is smaller than the image width, then no need to split
    # just add it to the line list and return
    if font.getsize(text)[0] <= max_width:
        lines.append(text)
    else:
        # split the line by spaces to get words
        words = text.split(" ")
        i = 0
        # append every word to a line while its width is shorter than the image width
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


def publish_froge_of_the_day(event, _context) -> base64:
    print("Start")
    print(event)

    # Decode envent data to get channel_id
    pubsub_message = base64.b64decode(event["data"]).decode("utf-8")
    channel_id = json.loads(pubsub_message)["ChannelId"]
    message = json.loads(pubsub_message)["Message"]

    print(f"Channel id is: {channel_id}")

    # Generate the Froge of the Day with random quote
    random_image = f"{random.randint(1, 54):04.0f}.jpg"
    random_text = ""
    while len(random_text) > 120 or len(random_text) < 10:
        random_text_request = requests.get("https://programming-quotes-api.herokuapp.com/quotes/random")
        random_text = json.loads(random_text_request.content.decode("utf-8"))["en"]

    print(f"Quote of the day is: {random_text}")

    froge_of_the_day = auto_scale_text_over_image(Image.open(f"{IMAGE_FOLDER}{random_image}"), text=random_text)

    # Encode image to base64
    buffered = BytesIO()
    froge_of_the_day.save(buffered, format="JPEG")
    image_str = base64.b64encode(buffered.getvalue()).decode("UTF-8")

    print(str(image_str))

    # Google publisher config
    project_id = "archy-f06ed"
    topic_id = "channel_message_discord"
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_id)

    # Encode data
    data = {"ChannelId": channel_id, "Message": message, "Image": image_str}
    encoded_data = json.dumps(data, indent=2).encode("utf-8")

    # Publish the data
    print("Publishing data")
    publisher.publish(topic_path, encoded_data)

    print("Done!")
