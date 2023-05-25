from database.db_manager import DBManager
from database.model import Base, User as Userdb, Group as Groupdb, GroupUser as GroupUserdb, \
                           Message as Messagedb

from custom_logger import CustomLogger
logger = CustomLogger().setup()

testuser1 = None
testuser2 = None
testuser3 = None
testgroupuser1 = None
testgroupuser2 = None
testgroupuser3 = None
testgroup = None
testmsg1 = None
testmsg2 = None
testmsg3 = None
testmsg4 = None

def create():
    logger.info("creating test data")

    global testuser1, testuser2, testuser3, testgroup, testgroupuser1, testgroupuser2, testgroupuser3, testmsg1, testmsg2, testmsg3, testmsg4

    testuser1 = Userdb(username="The test user 1", email="thetestuser1@mail.com", publickey="some_key", salt="testusersalt", hashed_pw="abcde", token=f"usertesttoken1")
    DBManager.get_inst().session.add(testuser1)
    testuser2 = Userdb(username="The test user 2", email="thetestuser2@mail.com", publickey="some_key", salt="testusersalt", hashed_pw="abcde", token=f"usertesttoken2")
    DBManager.get_inst().session.add(testuser2)
    testuser3 = Userdb(username="The test user 3", email="thetestuser3@mail.com", publickey="some_key", salt="testusersalt", hashed_pw="abcde", token=f"usertesttoken3")
    DBManager.get_inst().session.add(testuser3)
    testuser4 = Userdb(username="The test user 4", email="thetestuser4@mail.com", publickey="some_key", salt="testusersalt", hashed_pw="abcde", token=f"usertesttoken4")
    DBManager.get_inst().session.add(testuser4)

    testgroup = Groupdb(is_privatechat=False, groupname="The test group", description="A group for testing")
    DBManager.get_inst().session.add(testgroup)

    testgroupuser1 = GroupUserdb(isadmin=False)
    DBManager.get_inst().session.add(testgroupuser1)
    testgroupuser2 = GroupUserdb(isadmin=True)
    DBManager.get_inst().session.add(testgroupuser2)
    testgroupuser3 = GroupUserdb(isadmin=True)
    DBManager.get_inst().session.add(testgroupuser3)
    testgroupuser4 = GroupUserdb(isadmin=True)
    DBManager.get_inst().session.add(testgroupuser4)

    testmsg1 = Messagedb(content="This is the first test message!")
    DBManager.get_inst().session.add(testmsg1)
    testmsg2 = Messagedb(content="This is the second test message!")
    DBManager.get_inst().session.add(testmsg2)
    testmsg3 = Messagedb(content="This is the third test message!")
    DBManager.get_inst().session.add(testmsg3)
    testmsg4 = Messagedb(content="This is the last test message!")
    DBManager.get_inst().session.add(testmsg4)

    DBManager.get_inst().commit()

    testuser1.groupusers.append(testgroupuser1)
    testgroup.groupusers.append(testgroupuser1)

    testuser2.groupusers.append(testgroupuser2)
    testgroup.groupusers.append(testgroupuser2)

    testuser3.groupusers.append(testgroupuser3)
    testgroup.groupusers.append(testgroupuser3)

    testuser4.groupusers.append(testgroupuser4)
    testgroup.groupusers.append(testgroupuser4)

    testgroupuser3.messages.append(testmsg1)
    testgroup.groupmessages.append(testmsg1)

    testgroupuser1.messages.append(testmsg2)
    testgroup.groupmessages.append(testmsg2)

    testgroupuser3.messages.append(testmsg3)
    testgroup.groupmessages.append(testmsg3)

    testgroupuser2.messages.append(testmsg4)
    testgroup.groupmessages.append(testmsg4)

    DBManager.get_inst().commit()
