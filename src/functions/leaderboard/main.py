from typing import Any, Optional, Tuple

import flask
import functions_framework
from google.cloud.firestore_v1.client import Client
from google.cloud.firestore_v1.document import DocumentReference, DocumentSnapshot


@functions_framework.http
def leaderboard(request: flask.Request) -> Tuple[str, int]:  # pylint: disable=W0622
    """Return the current server leaderboard url."""

    request_json: Optional[Any] = request.get_json(silent=True)
    if request_json:
        server_id = request_json.get("server_id", None)

        if not server_id:
            print("Exit: Missing data in payload")
            return "", 200

        database: Client = Client(project="archy-f06ed")
        doc_ref: DocumentReference = database.collection("servers").document(server_id)
        doc: DocumentSnapshot = doc_ref.get()

        return str(doc.get("url"))

    return "", 200
