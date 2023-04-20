import pytest
import requests

from tests import testdata
from custom_logger import CustomLogger
logger = CustomLogger().setup()

def test_user_get1(server):
    resp = requests.get(f"{server}/api/user/test1", timeout=5)
    assert not resp.json()["error"]
    user = resp.json()["data"]
    assert user["username"] == "The test user 1"
    logger.debug(f"testuser1: {user}")

def test_user_get2(server):
    resp = requests.get(f"{server}/api/user/test2", timeout=5)
    assert not resp.json()["error"]
    user = resp.json()["data"]
    assert user["username"] == "The test user 2"
    logger.debug(f"testuser2: {user}")

def test_user_get3(server):
    resp = requests.get(f"{server}/api/user/test3", timeout=5)
    assert not resp.json()["error"]
    user = resp.json()["data"]
    assert user["username"] == "The test user 3"
    logger.debug(f"testuser3: {user}")

def test_group_get(server):
    resp = requests.get(f"{server}/api/group/test", timeout=5)
    assert not resp.json()["error"]
    group = resp.json()["data"]
    assert group["groupname"] == testdata.testgroup.groupname
    assert group["description"] == testdata.testgroup.description
    logger.debug(f"testgroup: {group}")

def test_message_get1(server):
    resp = requests.get(f"{server}/api/message/test1", timeout=5)
    assert not resp.json()["error"]
    message = resp.json()["data"]
    assert message["content"] == testdata.testmsg1.content
    logger.debug(f"testmsg1: {message}")

def test_message_get2(server):
    resp = requests.get(f"{server}/api/message/test2", timeout=5)
    assert not resp.json()["error"]
    message = resp.json()["data"]
    assert message["content"] == testdata.testmsg2.content
    logger.debug(f"testmsg2: {message}")

def test_message_get3(server):
    resp = requests.get(f"{server}/api/message/test3", timeout=5)
    assert not resp.json()["error"]
    message = resp.json()["data"]
    assert message["content"] == testdata.testmsg3.content
    logger.debug(f"testmsg3: {message}")

def test_message_get4(server):
    resp = requests.get(f"{server}/api/message/test4", timeout=5)
    assert not resp.json()["error"]
    message = resp.json()["data"]
    assert message["content"] == testdata.testmsg4.content
    logger.debug(f"testmsg4: {message}")
