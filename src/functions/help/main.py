from typing import Any, Generator, Optional, Tuple

import flask
import functions_framework
from google.cloud.firestore_v1.client import Client
from google.cloud.firestore_v1.collection import CollectionReference
from google.cloud.firestore_v1.document import DocumentSnapshot


@functions_framework.http
def help(request: flask.Request) -> Tuple[str, int]:  # pylint: disable=W0622
    """Return the list of all actived functions."""

    request_json: Optional[Any] = request.get_json(silent=True)
    if request_json:
        server_id = request_json.get("server_id", None)

        if not server_id:
            print("Exit: Missing data")
            return "", 200

        database: Client = Client(project="archy-f06ed")
        function_collection: CollectionReference = (
            database.collection("servers").document(server_id).collection("functions")
        )
        docs: Generator[DocumentSnapshot, Any, None] = function_collection.where("active", "==", True).stream()

        return "\n".join([f"!{doc.id : <10} -> {doc.get('description') : >10}" for doc in docs])

    return "", 200
