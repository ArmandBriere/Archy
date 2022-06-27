# pylint: disable=C0103

import json

from google.cloud.pubsub_v1 import PublisherClient
from google.cloud.pubsub_v1.publisher.futures import Future

PROJECT_ID = "archy-f06ed"
TOPIC_ID = "channel_message_discord"

if __name__ == "__main__":
    publisher = PublisherClient()
    topic_path = publisher.topic_path(PROJECT_ID, TOPIC_ID)

    data = {
        "channel_id": "<INSERT_CHANNEL_ID>",
        "message": "Channel message!",
    }

    # Data must be a bytestring
    user_encode_data = json.dumps(data, indent=2).encode("utf-8")

    # When you publish a message, the client returns a future.
    future: Future = publisher.publish(topic_path, user_encode_data)

    print(f"Message id: {future.result()}")
    print(f"Published message to {topic_path}.")
