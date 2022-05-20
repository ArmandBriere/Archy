import json
import os
import time

import firebase_admin
import functions_framework
from firebase_admin import credentials, firestore


@functions_framework.http
def exp(request):
    """HTTP Cloud Function."""
    service_account_info = os.environ["GOOGLE_APPLICATION_CREDENTIALS"]
    creds = credentials.Certificate(json.loads(service_account_info))
    app = firebase_admin.initialize_app(creds, name=str(time.time()))

    request_json = request.get_json(silent=True)
    if request_json:
        name = request_json.get("name", None)
        database = firestore.client(app)
        doc_ref = database.collection("users").document(name)
        doc = doc_ref.get()
        if doc.exists:
            doc_ref.update({"exp": firestore.Increment(1)})  # pylint: disable=E1101
        else:
            doc_ref.set({"exp": 1})
    return f"Congratz <@{name}>! You have more exp now!"
