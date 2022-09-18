import json
from time import sleep
from typing import Any, Generator

import firebase_admin
from firebase_admin import credentials, firestore
from google.cloud.firestore_v1.client import Client
from google.cloud.firestore_v1.document import DocumentSnapshot
from google.cloud.pubsub_v1 import PublisherClient
from google.cloud.pubsub_v1.publisher.futures import Future


PROJECT_ID = "archy-f06ed"
TOPIC_ID = "update_user_role"


if __name__ == "__main__":
    creds = credentials.Certificate("../../src/key.json")
    firebase_admin.initialize_app(creds)

    database: Client = firestore.client()

    servers: Generator[DocumentSnapshot, Any, None] = (
        database.collection("servers").stream()
    )

    for server in servers:

        print(f"Register commands for server {server.id}")

        