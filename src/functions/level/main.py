import json
from typing import Any, Dict, Optional, Tuple

import flask
import functions_framework
import names
from google.cloud.firestore import Client
from google.cloud.firestore_v1.base_document import DocumentSnapshot
from google.cloud.firestore_v1.collection import CollectionReference
from google.cloud.firestore_v1.document import DocumentReference
from google.cloud.pubsub_v1 import PublisherClient
from google.cloud.pubsub_v1.publisher.futures import Future


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
            return ":|", 200

        # If a user is mentionned, get that user's level
        mentions = request_json.get("mentions", None)
        if mentions and mentions[0]:
            user_id = str(mentions[0])

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

            payload = {
                "username": username,
                "avatar_url": avatar_url,
                "rank": rank,
                "level": current_level,
                "percent": round(percent),
            }

            publish_generate_image(channel_id, payload)
            return f"Give me a minute, {names.get_first_name()} is working on it!", 200

        return f"... Wait a minute, Who is <@{user_id}>", 200

    return ":|", 200


def publish_generate_image(channel_id: str, payload: Dict[str, Any]) -> None:
    """Publish image to generate_level_image."""

    project_id = "archy-f06ed"
    topic_id = "generate_level_image"
    publisher = PublisherClient()
    topic_path: str = publisher.topic_path(project_id, topic_id)

    data = {"channel_id": channel_id, "payload": payload}
    encoded_data = json.dumps(data, indent=2).encode("utf-8")

    print("Publishing data")
    future: Future = publisher.publish(topic_path, encoded_data)

    print(f"Message id: {future.result()}")
    print(f"Published message to {topic_path}.")
