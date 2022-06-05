import json
import os
import random
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
            exp_toward_next_level = doc.get("exp_toward_next_level")
            level = doc.get("level")

            exp_needed_to_level_up = 5 * (level**2) + (50 * level) + 100 - exp_toward_next_level

            added_exp = random.randint(45, 75)

            if added_exp >= exp_needed_to_level_up:
                doc_ref.update({"level": firestore.Increment(1)})  # pylint: disable=E1101
                doc_ref.update({"exp_toward_next_level": added_exp - exp_needed_to_level_up})  # pylint: disable=E1101
            else:
                doc_ref.update({"exp_toward_next_level": firestore.Increment(added_exp)})  # pylint: disable=E1101
            doc_ref.update({"total_exp": firestore.Increment(added_exp)})  # pylint: disable=E1101

        else:
            doc_ref.set({"total_exp": 0, "exp_toward_next_level": 0, "level": 0})

    return f"Congratz <@{name}>! You have more exp now!"
