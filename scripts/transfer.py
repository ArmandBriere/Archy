import json
import requests
import firebase_admin
from firebase_admin import credentials, firestore


SERVER_ID = 755106635885838477

DISCORD_IMAGE_URL_PREFIX = "https://cdn.discordapp.com/avatars/"
DISCORD_IMAGE_URL_SUFIX = ".webp?size=1024"


class User:
    def __init__(self, user_id, username, exp_toward_next_level, level, total_exp, message_count, avatar_id) -> None:
        self.user_id = user_id
        self.username = username
        self.exp_toward_next_level = exp_toward_next_level
        self.level = level
        self.total_exp = total_exp
        self.avatar_id = avatar_id
        self.message_count = message_count
        self.avatar_url = f"{DISCORD_IMAGE_URL_PREFIX}{self.user_id}/{self.avatar_id}{DISCORD_IMAGE_URL_SUFIX}"

    def get_data(self):
        data = {
            "username": self.username,
            "exp_toward_next_level": self.exp_toward_next_level,
            "level": self.level,
            "total_exp": self.total_exp,
            "message_count": self.message_count,
            "avatar_url": self.avatar_url,
        }
        return data


if __name__ == "__main__":
    creds = credentials.Certificate("../src/key.json")
    firebase_admin.initialize_app(creds)

    response = requests.get(f"https://mee6.xyz/api/plugins/levels/leaderboard/{SERVER_ID}")

    data = response.json()
    with open("data.json", "w") as file:
        json.dump(response.json(), file)

    database = firestore.client()

    for user in data["players"]:
        user_id = user["id"]
        username = user["username"]
        exp_toward_next_level = user["detailed_xp"][0]
        level = user["level"]
        total_exp = user["detailed_xp"][2]
        message_count = user["message_count"]
        avatar_id = user["avatar"]

        current_user = User(user_id, username, exp_toward_next_level, level, total_exp, message_count, avatar_id)

        print(f"Addind data for {username}", end="")
        database.collection("servers").document(SERVER_ID).collection("users").document(current_user.user_id).set(
            current_user.get_data()
        )
        print(" - Done")
