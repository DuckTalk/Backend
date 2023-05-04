import pytest
import requests

from custom_logger import CustomLogger
logger = CustomLogger().setup()

message_data = {}

@pytest.mark.order(1)
def test_message_post(server, testuser, testuser2):
    global message_data
    message_data = {
        "sender_id": testuser["user_id"],
        "receiver": {
            "type": "user",
            "user_id": testuser2["user_id"]
        },
        "content": "This is a message for pytest"
    }

    post_payload = {
        "data": message_data
    }
    resp = requests.post(f"{server}/api/message", json=post_payload, timeout=5)
    assert not resp.json()["error"], resp.json()["data"]
    assert isinstance(resp.json()["data"]["message_id"], int)
    message_data["message_id"] = resp.json()["data"]["message_id"]

@pytest.mark.order(2)
def test_message_get(server):
    resp = requests.get(f"{server}/api/message/{message_data['message_id']}", timeout=5)
    assert not resp.json()["error"], resp.json()["data"]
    message = resp.json()["data"]
    assert message["message_id"] == message_data["message_id"]
    assert message["sender_id"] == message_data["sender_id"]
    assert message["receiver"]["type"] == message_data["receiver"]["type"]
    assert message["receiver"]["user_id"] == message_data["receiver"]["user_id"]
    assert message["content"] == message_data["content"]
