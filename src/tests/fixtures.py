from threading import Thread
from time import sleep

import requests
import pytest

@pytest.fixture
def server():
    import app
    Thread(target=app.run_app, args=(["--dbfile", "src/tests/test.db", "-p", "2007"],), daemon=True).start()
    sleep(0.5)
    yield "http://ableytner.ddns.net:2007"

@pytest.fixture
def testuser(server):
    user_data = {
        "username": "Test User",
        "email": "testuser1@mail.com",
        "pw_hash": "abcde",
        "salt": "some_salt"
    }
    post_payload = {
        "data": user_data
    }
    resp = requests.post(f"{server}/api/user", json=post_payload, timeout=5)
    assert not resp.json()["error"], resp.json()["data"]
    assert isinstance(resp.json()["data"]["user_id"], int)
    user_data["user_id"] = resp.json()["data"]["user_id"]

    yield user_data

@pytest.fixture
def testuser2(server):
    user_data = {
        "username": "Test User",
        "email": "testuser2@mail.com",
        "pw_hash": "abcde",
        "salt": "some_salt"
    }
    post_payload = {
        "data": user_data
    }
    resp = requests.post(f"{server}/api/user", json=post_payload, timeout=5)
    assert not resp.json()["error"], resp.json()["data"]
    assert isinstance(resp.json()["data"]["user_id"], int)
    user_data["user_id"] = resp.json()["data"]["user_id"]

    yield user_data
