import base64
import json
import random
from datetime import datetime

from google.cloud.firestore import Increment
from google.cloud.firestore_v1.base_document import DocumentSnapshot
from google.cloud.firestore_v1.batch import WriteBatch
from google.cloud.firestore_v1.client import Client
from google.cloud.firestore_v1.collection import CollectionReference
from google.cloud.firestore_v1.document import DocumentReference
from google.cloud.functions.context import Context
from google.cloud.pubsub_v1 import PublisherClient
from google.cloud.pubsub_v1.publisher.futures import Future

DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
TMP_FILE_PATH = "/tmp/tmp.json"


def exp(event: dict, _context: Context):
    """Increase the user experience on firestore."""

    pubsub_message = json.loads(base64.b64decode(event["data"]).decode("utf-8"))
    print(pubsub_message)

    print("Start")

    if pubsub_message:
        print("Parse json payload")

        user_id = pubsub_message.get("user_id", None)
        username = pubsub_message.get("username", None)
        avatar_url = pubsub_message.get("avatar_url", None)
        server_id = pubsub_message.get("server_id", None)
        server_name = pubsub_message.get("server_name", None)

        if not user_id or not username or not server_id or not server_name:
            print("Exit: Missing data in payload")
            return "", 200

        database: Client = Client(project="archy-f06ed")

        user_collection: CollectionReference = database.collection("servers").document(server_id).collection("users")
        doc_ref: DocumentReference = user_collection.document(user_id)
        doc: DocumentSnapshot = doc_ref.get()

        # Start a batch to write all changes at once
        batch: WriteBatch = database.batch()

        # Increase exp
        if doc.exists:
            last_message_timestamp: str = doc.get("last_message_timestamp")

            time_diff_in_sec: float = (
                datetime.now() - datetime.strptime(last_message_timestamp, DATETIME_FORMAT)
            ).total_seconds()

            # Only get exp once per minute
            if time_diff_in_sec < 60:
                print(f"Exit: Too soon - {(60 - time_diff_in_sec):.0f} sec!")
                return "", 200

            exp_toward_next_level: int = doc.get("exp_toward_next_level")
            level: int = doc.get("level")

            exp_needed_to_level_up: int = 5 * (level**2) + (50 * level) + 100 - exp_toward_next_level

            added_exp: int = random.randint(45, 75)

            batch.update(doc_ref, ({"message_count": Increment(1)}))

            if added_exp >= exp_needed_to_level_up:
                print(f"Update: level up user {user_id} to level {level+1} in {server_name}")

                batch.update(doc_ref, ({"level": Increment(1)}))
                batch.update(doc_ref, ({"exp_toward_next_level": added_exp - exp_needed_to_level_up}))

                send_message_to_user(
                    user_id, f"I'm so proud of you... You made it to level {level+1} in {server_name}!"
                )
                update_user_roles(server_id, user_id)

            else:
                print(f"Update: Increase {user_id}'s exp")

                batch.update(doc_ref, ({"exp_toward_next_level": Increment(added_exp)}))

            batch.update(
                doc_ref,
                (
                    {
                        "avatar_url": avatar_url,
                        "total_exp": Increment(added_exp),
                        "last_message_timestamp": datetime.now().strftime(DATETIME_FORMAT),
                    }
                ),
            )

        # Create the user
        else:
            print(f"Create: New user {user_id}")

            batch.set(
                doc_ref,
                {
                    "total_exp": 0,
                    "exp_toward_next_level": 0,
                    "level": 0,
                    "message_count": 0,
                    "last_message_timestamp": datetime.now().strftime(DATETIME_FORMAT),
                    "username": username,
                    "avatar_url": avatar_url,
                },
            )

        batch.commit()

    print("Done")
    return "", 200


def send_message_to_user(user_id: str, message: str) -> None:
    """Send a private message to a user by calling a cloud function."""

    print(f"Private Message: Sending to user {user_id}")

    # Publisher setup
    project_id = "archy-f06ed"
    topic_id = "private_message_discord"
    publisher = PublisherClient()
    topic_path: str = publisher.topic_path(project_id, topic_id)

    # Data must be a bytestring
    data = {"user_id": user_id, "message": message}
    user_encode_data: str = json.dumps(data, indent=2).encode("utf-8")

    # When you publish a message, the client returns a future.
    future: Future = publisher.publish(topic_path, user_encode_data)

    print(f"Message id: {future.result()}")
    print(f"Published message to {topic_path}.")


def update_user_roles(server_id: str, user_id: str) -> None:
    """Publish a pubsub message to update_user_role."""

    print(f"Update user role for {user_id}")

    # Publisher setup
    project_id = "archy-f06ed"
    topic_id = "update_user_role"
    publisher = PublisherClient()
    topic_path: str = publisher.topic_path(project_id, topic_id)

    # Data must be a bytestring
    data = {"server_id": server_id, "user_id": user_id}
    user_encode_data: str = json.dumps(data, indent=2).encode("utf-8")

    # When you publish a message, the client returns a future.
    future: Future = publisher.publish(topic_path, user_encode_data)

    print(f"Message id: {future.result()}")
    print(f"Published message to {topic_path}.")
