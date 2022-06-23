import flask
import functions_framework
from google.cloud import firestore
from google.cloud.firestore_v1.collection import CollectionReference


@functions_framework.http
def level(request: flask.Request):
    """Return the level of a user."""

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

        database = firestore.Client(project="archy-f06ed")
        collection: CollectionReference = database.collection("servers").document(server_id).collection("users")
        doc_ref = collection.document(name)
        doc = doc_ref.get()

        if doc.exists:
            current_level = doc.get("level")
            rank = len(collection.where("total_exp", ">", doc.get("total_exp")).get()) + 1

            return f"<@{name}> is level {current_level}! Rank {rank}"

        return f"... Wait a minute, Who is <@{name}>"

    return ":|"
