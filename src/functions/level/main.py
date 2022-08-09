import base64
import json
import os
from typing import Any, Optional, Tuple

import flask
import functions_framework
from google.cloud.firestore import Client
from google.cloud.firestore_v1.base_document import DocumentSnapshot
from google.cloud.firestore_v1.collection import CollectionReference
from google.cloud.firestore_v1.document import DocumentReference
from google.cloud.pubsub_v1 import PublisherClient
from google.cloud.pubsub_v1.publisher.futures import Future
from html2image import Html2Image
from jinja2 import Template


@functions_framework.http
def level(request: flask.Request) -> Tuple[str, int]:
    """Return the level of a user."""

    request_json: Optional[Any] = request.get_json(silent=True)
    if request_json:
        user_id = request_json.get("user_id", None)
        server_id = request_json.get("server_id", None)
        channel_id = request_json.get("channel_id", None)

        if not user_id or not server_id or not channel_id:
            print("Exit: Missing data in payload")
            return "", 200

        # If a user is mentionned, get that user's level
        mentions = request_json.get("mentions", None)
        if mentions and mentions[0]:
            user_id = str(mentions[0])
        if not user_id:
            return ":|", 200

        database: Client = Client(project="archy-f06ed")
        collection: CollectionReference = database.collection("servers").document(server_id).collection("users")
        doc_ref: DocumentReference = collection.document(user_id)
        doc: DocumentSnapshot = doc_ref.get()

        if doc.exists:
            current_level: int = doc.get("level")
            rank: int = len(collection.where("total_exp", ">", doc.get("total_exp")).get()) + 1

            username: str = doc.get("username")
            avatar_url: str = doc.get("avatar_url")
            exp_toward_next_level: int = doc.get("exp_toward_next_level")

            level_exp_needed = 5 * (current_level**2) + (50 * current_level) + 100
            percent = exp_toward_next_level / level_exp_needed * 100

            image_base64 = generate_image(username, avatar_url, rank, current_level, percent)
            publish_message_discord(channel_id, image_base64)

        return f"... Wait a minute, Who is <@{user_id}>", 200

    return ":|", 200


def generate_image(username: str, avatar_url: str, rank: int, level: int, percent: int) -> str:
    save_path = f"{username}.png"

    hti = Html2Image()

    if not os.path.exists(save_path):

        with open("./templates/level.html") as template:
            tm = Template(template.read())
            hti.screenshot(
                html_str=tm.render(
                    username=username, avatar_url=avatar_url, rank=rank, level=level, percent=percent
                ),
                save_as=save_path,
                size=(1680, 720),
            )

    with open(save_path, "rb") as img_file:
        b64_string = base64.b64encode(img_file.read())

    return b64_string


def publish_message_discord(channel_id: str, image_str: str = "") -> None:
    """Publish image to channel_message_discord."""

    if len(image_str) == 0:
        print("Exit: No image provided")
        return

    project_id = "archy-f06ed"
    topic_id = "channel_message_discord"
    publisher = PublisherClient()
    topic_path: str = publisher.topic_path(project_id, topic_id)

    data = {"channel_id": channel_id, "image": image_str}
    encoded_data = json.dumps(data, indent=2).encode("utf-8")

    print("Publishing data")
    future: Future = publisher.publish(topic_path, encoded_data)

    print(f"Message id: {future.result()}")
    print(f"Published message to {topic_path}.")
