import pytest
import requests

from custom_logger import CustomLogger
logger = CustomLogger().setup()

def test_message_fail_missingkeys(server, testuser, testuser2):
    message_data = {
        "receiver": {
            "type": "user",
            "user_id": testuser2["user_id"]
        },
        "content": "This is a message for pytest"
    }
    resp = requests.post(f"{server}/api/message", json={"data": message_data}, timeout=5)
    assert resp.json()["error"], resp.json()["data"]
    assert resp.json()["data"] == "Missing key 'sender_id'"

    message_data = {
        "sender_id": testuser["user_id"],
        "content": "This is a message for pytest"
    }
    resp = requests.post(f"{server}/api/message", json={"data": message_data}, timeout=5)
    assert resp.json()["error"], resp.json()["data"]
    assert resp.json()["data"] == "Missing key 'receiver'"

    message_data = {
        "sender_id": testuser["user_id"],
        "receiver": {
            "user_id": testuser2["user_id"]
        },
        "content": "This is a message for pytest"
    }
    resp = requests.post(f"{server}/api/message", json={"data": message_data}, timeout=5)
    assert resp.json()["error"], resp.json()["data"]
    assert resp.json()["data"] == "Missing key 'type'"

    message_data = {
        "sender_id": testuser["user_id"],
        "receiver": {
            "type": "user"
        },
        "content": "This is a message for pytest"
    }
    resp = requests.post(f"{server}/api/message", json={"data": message_data}, timeout=5)
    assert resp.json()["error"], resp.json()["data"]
    assert resp.json()["data"] == "Missing key 'user_id'"

    message_data = {
        "sender_id": testuser["user_id"],
        "receiver": {
            "type": "group"
        },
        "content": "This is a message for pytest"
    }
    resp = requests.post(f"{server}/api/message", json={"data": message_data}, timeout=5)
    assert resp.json()["error"], resp.json()["data"]
    assert resp.json()["data"] == "Missing key 'group_id'"

    message_data = {
        "sender_id": testuser["user_id"],
        "receiver": {
            "type": "user",
            "user_id": testuser2["user_id"]
        }
    }
    resp = requests.post(f"{server}/api/message", json={"data": message_data}, timeout=5)
    assert resp.json()["error"], resp.json()["data"]
    assert resp.json()["data"] == "Missing key 'content'"

def test_message_post_get(server, testuser, testuser2):
    message_data = {
        "sender_id": testuser["user_id"],
        "receiver": {
            "type": "user",
            "user_id": testuser2["user_id"]
        },
        "content": "This is a private message for pytest"
    }

    resp = requests.post(f"{server}/api/message", json={"data": message_data}, timeout=5)
    assert not resp.json()["error"], resp.json()["data"]
    assert isinstance(resp.json()["data"]["message_id"], int)
    message_data["message_id"] = resp.json()["data"]["message_id"]

    resp = requests.get(f"{server}/api/message/{message_data['message_id']}", timeout=5)
    assert not resp.json()["error"], resp.json()["data"]
    message = resp.json()["data"]
    assert message["message_id"] == message_data["message_id"]
    assert message["sender_id"] == message_data["sender_id"]
    assert message["receiver"]["type"] == message_data["receiver"]["type"]
    assert message["receiver"]["user_id"] == message_data["receiver"]["user_id"]
    assert message["content"] == message_data["content"]
