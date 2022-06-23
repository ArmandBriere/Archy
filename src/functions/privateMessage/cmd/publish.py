import json

from google.cloud import pubsub_v1

PROJECT_ID = "archy-f06ed"
TOPIC_ID = "private_message_discord"

publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(PROJECT_ID, TOPIC_ID)

data = {
    "UserId": "135048445097410560",
    "Message": "This is a private message !",
}

# Data must be a bytestring
user_encode_data = json.dumps(data, indent=2).encode("utf-8")

# When you publish a message, the client returns a future.
future = publisher.publish(topic_path, user_encode_data)
print(future.result())

print(f"Published messages to {topic_path}.")
