import json
import time
import os

import functions_framework
from flask import escape
import firebase_admin
from firebase_admin import credentials, firestore


@functions_framework.http
def level(request):
    """HTTP Cloud Function."""
    service_account_info = os.environ["GOOGLE_APPLICATION_CREDENTIALS"]
    creds = credentials.Certificate(json.loads(service_account_info))
    app = firebase_admin.initialize_app(creds, name=str(time.time()))

    request_json = request.get_json(silent=True)
    if request_json:
        name = request_json.get("name", None)
        db = firestore.client(app)
        doc_ref = db.collection("users").document(name)
        doc = doc_ref.get()
        if doc.exists:
            total_exp = doc.get("exp")
            return f"Sorry we are still working on level, <@{escape(name)}> has {total_exp} exp!"
        else:
            return f"... Wait a minute, Who are you <@{escape(name)}>"

    return ":|"
