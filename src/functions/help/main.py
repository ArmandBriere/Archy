from typing import Any, Generator, Optional, Tuple

import flask
import functions_framework
from google.cloud.firestore_v1.client import Client
from google.cloud.firestore_v1.collection import CollectionReference
from google.cloud.firestore_v1.document import DocumentSnapshot
from google.cloud.firestore_v1.query import Query


@functions_framework.http
def help(request: flask.Request) -> Tuple[str, int]:  # pylint: disable=W0622
    """Return the list of all actived functions."""

    request_json: Optional[Any] = request.get_json(silent=True)
    if request_json:
        server_id = request_json.get("server_id", None)
        server_name = request_json.get("server_name", None)

        if not server_id or not server_name:
            print("Exit: Missing data")
            return "", 200

        database: Client = Client(project="archy-f06ed")
        function_collection: CollectionReference = (
            database.collection("servers").document(server_id).collection("functions")
        )
        docs: Generator[DocumentSnapshot, Any, None] = (
            function_collection.where("active", "==", True).order_by("name", direction=Query.ASCENDING).stream()
        )

        response = f"Avaible commands for Archy in **{server_name}**:\n\n"
        for doc in docs:
            response += f"**!{doc.id}**\n"
            response += f"{doc.get('description')}\n"
            for example in doc.get("examples"):
                response += f"`{example}`\n"
            response += "\n"

        return response

    return "", 200
