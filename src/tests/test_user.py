import pytest
import requests

@pytest.mark.order(1)
def test_user_post(server):
    post_payload = {
        "type": "user",
        "data": {
            "username": "Test User",
            "email": "testuser2@mail.com",
            "pw_hash": "abcde",
            "salt": "some_salt"
        }
    }
    resp = requests.post(f"{server}/api/user", json=post_payload, timeout=5)
    assert not resp.json()["error"]
    assert resp.json()["data"] == {}

    get_payload = {
        "type": "user",
        "data": {
            "user_id": 1
        }
    }
    resp = requests.get(f"{server}/api/user", json=get_payload, timeout=5)
    assert not resp.json()["error"]
    user = resp.json()["data"]
    assert user["user_id"] == 1
    assert user["username"] == post_payload["data"]["username"]
    assert user["publickey"] != ""

@pytest.mark.order(2)
def test_user_get(server):
    resp = requests.get(f"{server}/api/user/1", timeout=5)
    assert not resp.json()["error"]
    user = resp.json()["data"]
    assert user["user_id"] == 1
    assert user["username"] == "Test User"
    assert user["publickey"] != ""

@pytest.mark.order(3)
def test_user_delete(server):
    get_payload = {
        "type": "user",
        "data": {
            "user_id": 1
        }
    }
    resp = requests.get(f"{server}/api/user", json=get_payload, timeout=5)
    assert not resp.json()["error"]
    user = resp.json()["data"]
    assert user["user_id"] == 1

    delete_payload = {
        "type": "user",
        "data": {
            "user_id": 1
        }
    }
    resp = requests.delete(f"{server}/api/user", json=delete_payload, timeout=5)
    assert not resp.json()["error"]
    assert resp.json()["data"] == {}

    get_payload = {
        "type": "user",
        "data": {
            "user_id": 1
        }
    }
    resp = requests.get(f"{server}/api/user", json=get_payload, timeout=5)
    assert resp.json()["error"]
    assert type(resp.json()["data"]) == str
