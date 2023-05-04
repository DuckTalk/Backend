import pytest
import requests

from custom_logger import CustomLogger
logger = CustomLogger().setup()

group_data = {
    "groupname": "Test Group",
    "description": "A test group for pytest"
}

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
