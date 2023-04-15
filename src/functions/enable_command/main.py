import json
import os
from typing import Any, Optional, Tuple

import firebase_admin
import flask
import functions_framework
from firebase_admin import firestore
from google.cloud.firestore_v1.base_document import DocumentSnapshot
from google.cloud.firestore_v1.collection import CollectionReference
from google.cloud.firestore_v1.document import DocumentReference

GOOGLE_APPLICATION_CREDENTIALS = json.loads(os.environ.get("GOOGLE_APPLICATION_CREDENTIALS"))


@functions_framework.http
def enable_command(request: flask.Request) -> Tuple[str, int]:

    request_json: Optional[Any] = request.get_json(silent=True)

    if request_json:
        command = request_json.get("command", None)
        enable = request_json.get("enable", None)
        if not command and not enable:
            return "Invalid request", 400
    else:
        return "Invalid request", 400

    certificate = firebase_admin.credentials.Certificate(GOOGLE_APPLICATION_CREDENTIALS)
    firebase_admin.initialize_app(certificate)

    database = firestore.client()

    server_list_collection: CollectionReference = database.collection("server_list")
    for server in server_list_collection.stream():
        server: DocumentSnapshot
        server_id: str = server.id
        server: DocumentReference = server_list_collection.document(server_id)
        functions_collection: CollectionReference = server.collection("functions")
        functions_collection.document(command).set({"enable": enable})

    return f"Command {'enabled' if enable else 'disabled'}", 200
