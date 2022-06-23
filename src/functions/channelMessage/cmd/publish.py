# pylint: disable=C0103

import json

from google.cloud import pubsub_v1

PROJECT_ID = "archy-f06ed"
TOPIC_ID = "channel_message_discord"

if __name__ == "__main__":
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(PROJECT_ID, TOPIC_ID)

    data = {
        "ChannelId": "<INSERT_CHANNEL_ID>",
        "Message": "Channel message!",
    }

    # Data must be a bytestring
    user_encode_data = json.dumps(data, indent=2).encode("utf-8")

    # When you publish a message, the client returns a future.
    future = publisher.publish(topic_path, user_encode_data)
    print(future.result())

    print(f"Published messages to {topic_path}.")
