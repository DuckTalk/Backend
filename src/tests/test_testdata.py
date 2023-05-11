import requests

from tests import testdata
from custom_logger import CustomLogger
logger = CustomLogger().setup()

def test_user_get(server):
    # --------------- Test user 1 ---------------
    resp = requests.get(f"{server}/api/user/test1", timeout=5)
    assert not resp.json()["error"]
    user = resp.json()["data"]
    assert user["username"] == "The test user 1"

    resp2 = requests.get(f"{server}/api/user/test1", timeout=5)
    assert not resp2.json()["error"]
    assert user["user_id"] == resp2.json()["data"]["user_id"] # check if the same user is returned both times

    # --------------- Test user 2 ---------------
    resp = requests.get(f"{server}/api/user/test2", timeout=5)
    assert not resp.json()["error"]
    user = resp.json()["data"]
    assert user["username"] == "The test user 2"

    resp2 = requests.get(f"{server}/api/user/test2", timeout=5)
    assert not resp2.json()["error"]
    assert user["user_id"] == resp2.json()["data"]["user_id"]

    # --------------- Test user 3 ---------------
    resp = requests.get(f"{server}/api/user/test3", timeout=5)
    assert not resp.json()["error"]
    user = resp.json()["data"]
    assert user["username"] == "The test user 3"

    resp2 = requests.get(f"{server}/api/user/test3", timeout=5)
    assert not resp2.json()["error"]
    assert user["user_id"] == resp2.json()["data"]["user_id"]

def test_group_get(server):
    resp = requests.get(f"{server}/api/group/test", timeout=5)
    assert not resp.json()["error"]
    group = resp.json()["data"]
    assert group["groupname"] == testdata.testgroup.groupname
    assert group["description"] == testdata.testgroup.description

    resp2 = requests.get(f"{server}/api/group/test", timeout=5)
    assert not resp2.json()["error"]
    assert group["group_id"] == resp2.json()["data"]["group_id"]

def test_message_get(server):
    # --------------- Test message 1 ---------------
    resp = requests.get(f"{server}/api/message/test1", timeout=5)
    assert not resp.json()["error"]
    message = resp.json()["data"]
    assert message["content"] == testdata.testmsg1.content

    resp2 = requests.get(f"{server}/api/message/test1", timeout=5)
    assert not resp2.json()["error"]
    assert message["message_id"] == resp2.json()["data"]["message_id"]

    # --------------- Test message 2 ---------------
    resp = requests.get(f"{server}/api/message/test2", timeout=5)
    assert not resp.json()["error"]
    message = resp.json()["data"]
    assert message["content"] == testdata.testmsg2.content

    resp2 = requests.get(f"{server}/api/message/test2", timeout=5)
    assert not resp2.json()["error"]
    assert message["message_id"] == resp2.json()["data"]["message_id"]

    # --------------- Test message 3 ---------------
    resp = requests.get(f"{server}/api/message/test3", timeout=5)
    assert not resp.json()["error"]
    message = resp.json()["data"]
    assert message["content"] == testdata.testmsg3.content

    resp2 = requests.get(f"{server}/api/message/test3", timeout=5)
    assert not resp2.json()["error"]
    assert message["message_id"] == resp2.json()["data"]["message_id"]

    # --------------- Test message 4 ---------------
    resp = requests.get(f"{server}/api/message/test4", timeout=5)
    assert not resp.json()["error"]
    message = resp.json()["data"]
    assert message["content"] == testdata.testmsg4.content

    resp2 = requests.get(f"{server}/api/message/test4", timeout=5)
    assert not resp2.json()["error"]
    assert message["message_id"] == resp2.json()["data"]["message_id"]
