import datetime
import json
import os
import random
import time

import firebase_admin
import functions_framework
from firebase_admin import credentials, firestore

DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"


@functions_framework.http
def exp(request):
    """Increase the user experience on firestore."""

    # Setup firestore connection
    service_account_info = os.environ["GOOGLE_APPLICATION_CREDENTIALS"]
    creds = credentials.Certificate(json.loads(service_account_info))
    app = firebase_admin.initialize_app(creds, name=str(time.time()))

    request_json = request.get_json(silent=True)
    if request_json:
        name = request_json.get("name", None)
        server_id = request_json.get("server_id", None)
        database = firestore.client(app)

        collection = database.collection("servers").document(server_id).collection("users")
        doc_ref = collection.document(name)
        doc = doc_ref.get()
        # Start a batch to write all changes at once
        batch = database.batch()

        # Increase exp
        if doc.exists:
            last_message_timestamp = doc.get("last_message_timestamp")

            time_diff_in_sec = (
                datetime.datetime.now() - datetime.datetime.strptime(last_message_timestamp, DATETIME_FORMAT)
            ).total_seconds()

            print(time_diff_in_sec)

            # Only get exp once per minute
            if time_diff_in_sec < 60:
                return f"You need to wait a bit more, come back in {(60 - time_diff_in_sec):.0f} sec!"

            exp_toward_next_level = doc.get("exp_toward_next_level")
            level = doc.get("level")

            exp_needed_to_level_up = 5 * (level**2) + (50 * level) + 100 - exp_toward_next_level

            added_exp = random.randint(45, 75)

            if added_exp >= exp_needed_to_level_up:
                batch.update(doc_ref, ({"level": firestore.Increment(1)}))  # pylint: disable=E1101
                batch.update(doc_ref, ({"exp_toward_next_level": added_exp - exp_needed_to_level_up}))
            else:
                batch.update(
                    doc_ref, ({"exp_toward_next_level": firestore.Increment(added_exp)})  # pylint: disable=E1101
                )

            update_user_ranks(database, batch)

            batch.update(
                doc_ref,
                (
                    {
                        "total_exp": firestore.Increment(added_exp),  # pylint: disable=E1101
                        "last_message_timestamp": datetime.datetime.now().strftime(DATETIME_FORMAT),
                    }
                ),
            )

        # Create the user
        else:
            batch.set(
                doc_ref,
                {
                    "total_exp": 0,
                    "exp_toward_next_level": 0,
                    "level": 0,
                    "rank": len(collection.get()) + 1,
                    "last_message_timestamp": datetime.datetime.now().strftime(DATETIME_FORMAT),
                },
            )

        batch.commit()

    return f"Congratz <@{name}>! You have more exp now!"


def update_user_ranks(database, batch):
    """Update all user ranks by descending total_exp."""

    users_ref = database.collection("users")
    users = users_ref.order_by("total_exp", direction=firestore.Query.DESCENDING).stream()  # pylint: disable=E1101

    for index, user in enumerate(users):
        batch.update(user.reference, {"rank": index + 1})
