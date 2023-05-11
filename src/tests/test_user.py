import pytest
import requests

from custom_logger import CustomLogger
logger = CustomLogger().setup()

def test_user_fail_missingkeys(server):
    user_data = {
        "email": "failuser@mail.com",
        "pw_hash": "abcde",
        "salt": "some_salt"
    }
    resp = requests.post(f"{server}/api/user", json={"data": user_data}, timeout=5)
    assert resp.json()["error"], resp.json()["data"]
    assert resp.json()["data"] == "Missing key 'username'"

    user_data = {
        "username": "Fail User",
        "pw_hash": "abcde",
        "salt": "some_salt"
    }
    resp = requests.post(f"{server}/api/user", json={"data": user_data}, timeout=5)
    assert resp.json()["error"], resp.json()["data"]
    assert resp.json()["data"] == "Missing key 'email'"

    user_data = {
        "username": "Fail User",
        "email": "failuser@mail.com",
        "salt": "some_salt"
    }
    resp = requests.post(f"{server}/api/user", json={"data": user_data}, timeout=5)
    assert resp.json()["error"], resp.json()["data"]
    assert resp.json()["data"] == "Missing key 'pw_hash'"

    user_data = {
        "username": "Fail User",
        "email": "failuser@mail.com",
        "pw_hash": "abcde",
    }
    resp = requests.post(f"{server}/api/user", json={"data": user_data}, timeout=5)
    assert resp.json()["error"], resp.json()["data"]
    assert resp.json()["data"] == "Missing key 'salt'"

def test_user_post_get_delete(server):
    user_data = {
        "username": "Test User",
        "email": "testuser2@mail.com",
        "pw_hash": "abcde",
        "salt": "some_salt"
    }

    # --------------- POST ---------------
    post_payload = {
        "data": user_data
    }
    resp = requests.post(f"{server}/api/user", json=post_payload, timeout=5)
    assert not resp.json()["error"], resp.json()["data"]
    assert isinstance(resp.json()["data"]["user_id"], int)
    user_data["user_id"] = resp.json()["data"]["user_id"]

    # --------------- GET ---------------
    resp = requests.get(f"{server}/api/user/{user_data['user_id']}", timeout=5)
    assert not resp.json()["error"], resp.json()["data"]
    user = resp.json()["data"]
    assert user["user_id"] == user_data["user_id"]
    assert user["username"] == user_data["username"]
    assert user["publickey"] != ""

    # --------------- DELETE ---------------
    resp = requests.delete(f"{server}/api/user/{user_data['user_id']}", timeout=5)
    assert not resp.json()["error"], resp.json()["data"]
    assert resp.json()["data"] == {}

    resp = requests.get(f"{server}/api/user/{user_data['user_id']}", timeout=5)
    assert resp.json()["error"], resp.json()["data"]
    assert isinstance(resp.json()["data"], str)
