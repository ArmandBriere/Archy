import json
import os

import google.auth.transport.requests
import google.oauth2.id_token
import requests

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "./key.json"
request = google.auth.transport.requests.Request()
FUNCTION_BASE_RUL = "https://us-central1-archy-f06ed.cloudfunctions.net/"
TOKEN = google.oauth2.id_token.fetch_id_token(request, f"{FUNCTION_BASE_RUL}archy_py")

r = requests.post(
    "https://us-central1-archy-f06ed.cloudfunctions.net/archy_py",
    headers={"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"},
    data=json.dumps({"name": "test"}),
)
r.status_code, r.reason
print(r.status_code, r.reason, r.content)
