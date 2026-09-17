import json
from fastapi.testclient import TestClient
from app import app  # replace 'app' with your python filename if different

client = TestClient(app)

# Load your local JSON file
with open("request.json", "r") as f:
    payload = json.load(f)

# Send the request directly to the app instance
response = client.post("/blogs", json=payload)

print("Status Code:", response.status_code)
print("Response Body:", response.json())