import json
import os
import time

import firebase_admin
import functions_framework
from firebase_admin import credentials, firestore


@functions_framework.http
def level(request):
    """Return the level of a user."""

    service_account_info = os.environ["GOOGLE_APPLICATION_CREDENTIALS"]
    creds = credentials.Certificate(json.loads(service_account_info))
    app = firebase_admin.initialize_app(creds, name=str(time.time()))

    request_json = request.get_json(silent=True)
    if request_json:
        name = request_json.get("name", None)
        server_id = request_json.get("server_id", None)

        # If a user is mentionned, get that user's level
        mentions = request_json.get("mentions", None)
        if mentions and mentions[0]:
            name = str(mentions[0])
        if not name:
            return ":|"

        database = firestore.client(app)
        collection = database.collection("servers").document(server_id).collection("users")
        doc_ref = collection.document(name)
        doc = doc_ref.get()

        if doc.exists:
            current_level = doc.get("level")
            rank = doc.get("rank")
            user_count = len(list(collection.get()))

            return f"<@{name}> is level {current_level}! Rank {rank}/{user_count}"

        return f"... Wait a minute, Who is <@{name}>"

    return ":|"
