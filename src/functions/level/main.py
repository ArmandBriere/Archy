from typing import Any, Optional, Tuple

import flask
import functions_framework
from google.cloud.firestore import Client
from google.cloud.firestore_v1.base_document import DocumentSnapshot
from google.cloud.firestore_v1.collection import CollectionReference
from google.cloud.firestore_v1.document import DocumentReference


@functions_framework.http
def level(request: flask.Request) -> Tuple[str, int]:
    """Return the level of a user."""

    request_json: Optional[Any] = request.get_json(silent=True)
    if request_json:
        username = request_json.get("username", None)
        server_id = request_json.get("server_id", None)

        # If a user is mentionned, get that user's level
        mentions = request_json.get("mentions", None)
        if mentions and mentions[0]:
            username = str(mentions[0])
        if not username:
            return ":|", 200

        database: Client = Client(project="archy-f06ed")
        collection: CollectionReference = database.collection("servers").document(server_id).collection("users")
        doc_ref: DocumentReference = collection.document(username)
        doc: DocumentSnapshot = doc_ref.get()

        if doc.exists:
            current_level: int = doc.get("level")
            rank: int = len(collection.where("total_exp", ">", doc.get("total_exp")).get()) + 1

            return f"<@{username}> is level {current_level}! Rank {rank}", 200

        return f"... Wait a minute, Who is <@{username}>", 200

    return ":|", 200
