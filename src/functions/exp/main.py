import json
import os
import random
import time
from datetime import datetime

import firebase_admin
import functions_framework
from firebase_admin import credentials, firestore
from google.cloud import pubsub_v1

DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
TMP_FILE_PATH = "/tmp/tmp.json"


@functions_framework.http
def exp(request):
    """Increase the user experience on firestore."""

    print("Start")

    # Setup firestore connection
    service_account_info = os.environ["GOOGLE_APPLICATION_CREDENTIALS"]
    creds = credentials.Certificate(json.loads(service_account_info))

    app = firebase_admin.initialize_app(creds, name=str(time.time()))

    request_json = request.get_json(silent=True)
    if request_json:
        print("Parse json payload")

        user_id = request_json.get("user_id", None)
        username = request_json.get("username", None)
        avatar_url = request_json.get("avatar_url", None)
        server_id = request_json.get("server_id", None)

        if not user_id or not username or not server_id:
            print("Exit: Missing data in payload")
            return "", 200

        database = firestore.client(app)

        collection = database.collection("servers").document(server_id).collection("users")
        doc_ref = collection.document(user_id)
        doc = doc_ref.get()

        # Start a batch to write all changes at once
        batch = database.batch()

        # Increase exp
        if doc.exists:
            last_message_timestamp = doc.get("last_message_timestamp")

            time_diff_in_sec = (
                datetime.now() - datetime.strptime(last_message_timestamp, DATETIME_FORMAT)
            ).total_seconds()

            # Only get exp once per minute
            if time_diff_in_sec < 60:
                print(f"Exit: Too soon - {(60 - time_diff_in_sec):.0f} sec!")
                return "", 200

            exp_toward_next_level = doc.get("exp_toward_next_level")
            level = doc.get("level")

            exp_needed_to_level_up = 5 * (level**2) + (50 * level) + 100 - exp_toward_next_level

            added_exp = random.randint(45, 75)

            if added_exp >= exp_needed_to_level_up:
                print(f"Update: level up user {user_id} to level {level+1}")

                batch.update(doc_ref, ({"level": firestore.Increment(1)}))  # pylint: disable=E1101
                batch.update(doc_ref, ({"exp_toward_next_level": added_exp - exp_needed_to_level_up}))

                send_message_to_user(user_id, f"I'm so proud of you... You made it to level {level+1}!")

            else:
                print(f"Update: Increase {user_id}'s exp")

                batch.update(
                    doc_ref, ({"exp_toward_next_level": firestore.Increment(added_exp)})  # pylint: disable=E1101
                )

            update_user_ranks(database.collection("servers").document(server_id), batch)

            batch.update(
                doc_ref,
                (
                    {
                        "total_exp": firestore.Increment(added_exp),  # pylint: disable=E1101
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
                    "rank": len(collection.get()) + 1,
                    "last_message_timestamp": datetime.now().strftime(DATETIME_FORMAT),
                    "username": username,
                    "avatar_url": avatar_url,
                },
            )

        batch.commit()

    print("Done")
    return "", 200


def update_user_ranks(database, batch):
    """Update all user ranks by descending total_exp."""

    users_ref = database.collection("users")
    users = users_ref.order_by("total_exp", direction=firestore.Query.DESCENDING).stream()  # pylint: disable=E1101

    for index, user in enumerate(users):
        batch.update(user.reference, {"rank": index + 1})


def send_message_to_user(user_id: str, message: str):
    """Send a private message to a user by calling a cloud function."""
    print(f"Private Message: Sending to user {user_id}")

    # Publisher setup
    project_id = "archy-f06ed"
    topic_id = "private_message_discord"
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_id)

    # Data must be a bytestring
    data = {"UserId": user_id, "Message": message}
    user_encode_data = json.dumps(data, indent=2).encode("utf-8")

    # When you publish a message, the client returns a future.
    future = publisher.publish(topic_path, user_encode_data)
    print(future.result())
    print("Private Message: Done")
