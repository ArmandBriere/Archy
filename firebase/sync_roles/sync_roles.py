import json
from time import sleep
from typing import Any, Generator

import firebase_admin
from firebase_admin import credentials, firestore
from google.cloud.firestore_v1.client import Client
from google.cloud.firestore_v1.document import DocumentSnapshot
from google.cloud.pubsub_v1 import PublisherClient
from google.cloud.pubsub_v1.publisher.futures import Future


SERVER_ID = "<SERVER_ID>"

PROJECT_ID = "archy-f06ed"
TOPIC_ID = "update_user_role"


if __name__ == "__main__":
    creds = credentials.Certificate("../../src/key.json")
    firebase_admin.initialize_app(creds)

    database: Client = firestore.client()

    users: Generator[DocumentSnapshot, Any, None] = (
        database.collection("servers").document(SERVER_ID).collection("users").stream()
    )

    for user in users:

        print(f"Adding role to {user.id}")
        publisher = PublisherClient()
        topic_path = publisher.topic_path(PROJECT_ID, TOPIC_ID)

        data = {
            "server_id": SERVER_ID,
            "user_id": str(user.id),
        }
        encoded_data = json.dumps(data, indent=2).encode("utf-8")

        future: Future = publisher.publish(topic_path, encoded_data)

        print(f"Message id: {future.result()}")
        print(f"Published message to {topic_path}.")

        sleep(1)
