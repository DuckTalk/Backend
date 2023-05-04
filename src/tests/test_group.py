import pytest
import requests

from custom_logger import CustomLogger
logger = CustomLogger().setup()

group_data = {
    "groupname": "Test Group",
    "description": "A test group for pytest"
}

def test_group_fail_missingkeys(server, testuser):
    group_data = {
        "description": "A test group for pytest",
        "user_id": testuser["user_id"]
    }
    resp = requests.post(f"{server}/api/group", json={"data": group_data}, timeout=5)
    assert resp.json()["error"], resp.json()["data"]
    assert resp.json()["data"] == "Missing key 'groupname'"

    group_data = {
        "groupname": "Test Group",
        "user_id": testuser["user_id"]
    }
    resp = requests.post(f"{server}/api/group", json={"data": group_data}, timeout=5)
    assert resp.json()["error"], resp.json()["data"]
    assert resp.json()["data"] == "Missing key 'description'"

    group_data = {
        "groupname": "Test Group",
        "description": "A test group for pytest"
    }
    resp = requests.post(f"{server}/api/group", json={"data": group_data}, timeout=5)
    assert resp.json()["error"], resp.json()["data"]
    assert resp.json()["data"] == "Missing key 'user_id'"

def test_group_fail_invalidid(server):
    for user_id in [0, -1, "test", ""]:
        group_data = {
            "groupname": "Test Group",
            "description": "A test group for pytest",
            "user_id": user_id
        }
        resp = requests.post(f"{server}/api/group", json={"data": group_data}, timeout=5)
        assert resp.json()["error"], resp.json()["data"]
        assert resp.json()["data"] == f"User with user_id {user_id} not found"

@pytest.mark.order(1)
def test_group_post(server, testuser):
    global group_data
    group_data["user_id"] = testuser["user_id"]
    post_payload = {
        "data": group_data
    }
    resp = requests.post(f"{server}/api/group", json=post_payload, timeout=5)
    assert not resp.json()["error"], resp.json()["data"]
    assert isinstance(resp.json()["data"]["group_id"], int)
    group_data["group_id"] = resp.json()["data"]["group_id"]

@pytest.mark.order(2)
def test_group_get(server):
    resp = requests.get(f"{server}/api/group/{group_data['group_id']}", timeout=5)
    assert not resp.json()["error"], resp.json()["data"]
    group = resp.json()["data"]
    assert group["group_id"] == group_data["group_id"]
    assert group["groupname"] == group_data["groupname"]
    assert group["description"] == group_data["description"]
    assert len(group["members"]) == 1
    assert group["members"]["0"]["user_id"] == group_data["user_id"]
