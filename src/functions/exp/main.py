import json
import time
import os

import functions_framework
from flask import escape
import firebase_admin
from firebase_admin import credentials, firestore


@functions_framework.http
def exp(request):
    """HTTP Cloud Function."""
    print("Get creds")
    service_account_info = os.environ["GOOGLE_APPLICATION_CREDENTIALS"]
    creds = credentials.Certificate(json.loads(service_account_info))
    print("Start firebase app init")
    app = firebase_admin.initialize_app(creds, name=str(time.time()))

    request_json = request.get_json(silent=True)
    name = ""
    print("If request")
    if request_json:
        name = request_json.get("name", None)
        print(f"name : {name}")
        print("Start db client")
        db = firestore.client(app)
        print("Get collection")
        doc_ref = db.collection("users").document(name)
        print("Increment value")
        doc = doc_ref.get()
        if doc.exists:
            print("doc exists")
            doc_ref.update({"exp": firestore.Increment(1)})
        else:
            print("doc do not exists")
            doc_ref.set({"exp": 1})
    print("DONE")
    return "Congratz <@{}>! You have more exp now!".format(escape(name))


if __name__ == "__main__":
    print(exp({"name": "tmp"}))
