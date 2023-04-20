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

def test_user_get2(server):
    resp = requests.get(f"{server}/api/user/test2", timeout=5)
    assert not resp.json()["error"]
    user = resp.json()["data"]
    assert user["username"] == "The test user 2"

def test_user_get3(server):
    resp = requests.get(f"{server}/api/user/test3", timeout=5)
    assert not resp.json()["error"]
    user = resp.json()["data"]
    assert user["username"] == "The test user 3"

def test_group_get(server):
    resp = requests.get(f"{server}/api/group/test", timeout=5)
    assert not resp.json()["error"]
    group = resp.json()["data"]
    assert group["groupname"] == testdata.testgroup.groupname
    assert group["description"] == testdata.testgroup.description
    logger.debug(group)
