import json
from typing import Any, Dict, Generator

import firebase_admin
from firebase_admin import credentials, firestore
from google.cloud.firestore_v1.client import Client
from google.cloud.firestore_v1.document import DocumentSnapshot


SERVERS = ["755106635885838477", "964701887540645908"]


def register_or_update_command(command: Dict, server_id: str, database: Client):

    doc_ref = database.collection("servers").document(server_id).collection("functions").document(command.get("name"))

    if doc_ref.get().exists:
        print(f"Update command {command.get('name')} for server {server.id}")

        doc_ref.update(
            {
                "name": command.get("name"),
                "description": command.get("description"),
                "examples": command.get("examples"),
            }
        )
    else:
        print(f"Register command {command.get('name')} for server {server.id}")
        doc_ref.set(
            {
                "name": command.get("name"),
                "description": command.get("description"),
                "examples": command.get("examples"),
                "active": False,
            }
        )


if __name__ == "__main__":
    creds = credentials.Certificate("../../src/key.json")
    firebase_admin.initialize_app(creds)
    database: Client = firestore.client()

    with open("commands.json") as f:
        data = json.load(f)
        for server_id in SERVERS:
            server: Generator[DocumentSnapshot, Any, None] = database.collection("servers").document(server_id)

            for command in data.get("commands"):

                register_or_update_command(command, server_id, database)
