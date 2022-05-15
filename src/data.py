import requests
import google.auth
import google.auth.transport.requests

from google.oauth2 import service_account

credentials = service_account.Credentials.from_service_account_file(
    "key.json", scopes=["https://www.googleapis.com/auth/cloud-platform"]
)

print(credentials)
auth_req = google.auth.transport.requests.Request()
credentials.refresh(auth_req)
print(credentials.token)
print(credentials.valid)


endpoint = "https://us-central1-archy-f06ed.cloudfunctions.net/archy_py"
data = {"name": "test"}
headers = {"Authorization": f"Bearer {credentials.token}"}

resp = requests.post(endpoint, data=data, headers=headers)

print(resp)
print(resp.reason)
