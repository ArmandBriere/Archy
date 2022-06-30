from typing import Any, Optional, Tuple, Generator

import functions_framework
from google.cloud.firestore_v1.collection import CollectionReference
from google.cloud.firestore_v1.client import Client
from google.cloud.firestore_v1.base_document import DocumentSnapshot


@functions_framework.http
def hello(request) -> Tuple[str, int]:
    """Return the requested list of all actived function."""

    request_json: Optional[Any] = request.get_json(silent=True)

    if request_json:
        server_id = request_json.get("server_id", None)

        database: Client = Client(project="archy-f06ed")

        function_collection: CollectionReference = (
            database.collection("servers").document(server_id).collection("functions")
        )

        docs: Generator[DocumentSnapshot, Any, None] = function_collection.where("active", "==", True).stream()

        if not server_id:
            print("Exit: Missing data")
            return "", 200

        if docs.exists:
            return "\n".join([f'!{doc.id} -> {doc.get("description")}' for doc in docs])

    return "", 200
