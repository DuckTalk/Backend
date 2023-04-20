from database.db_manager import DBManager
from database.model import Base, User as Userdb, Group as Groupdb, GroupUser as GroupUserdb, \
                           Message as Messagedb

testuser1 = None
testuser2 = None
testuser3 = None
testgroupuser1 = None
testgroupuser2 = None
testgroupuser3 = None
testgroup = None

def create():
    global testuser1, testuser2, testuser3, testgroup, testgroupuser1, testgroupuser2, testgroupuser3
    testuser1 = Userdb(username="The test user 1", email="thetestuser1@mail.com", publickey="some_key", salt="testusersalt", hashed_pw="abcde", token=f"usertesttoken1")
    DBManager.get_inst().session.add(testuser1)
    testuser2 = Userdb(username="The test user 2", email="thetestuser2@mail.com", publickey="some_key", salt="testusersalt", hashed_pw="abcde", token=f"usertesttoken2")
    DBManager.get_inst().session.add(testuser2)
    testuser3 = Userdb(username="The test user 3", email="thetestuser3@mail.com", publickey="some_key", salt="testusersalt", hashed_pw="abcde", token=f"usertesttoken3")
    DBManager.get_inst().session.add(testuser3)

    testgroup = Groupdb(is_privatechat=False, groupname="The test group", description="A group for testing")
    DBManager.get_inst().session.add(testgroup)

    testgroupuser1 = GroupUserdb(isadmin=False)
    DBManager.get_inst().session.add(testgroupuser1)
    testgroupuser2 = GroupUserdb(isadmin=True)
    DBManager.get_inst().session.add(testgroupuser2)
    testgroupuser3 = GroupUserdb(isadmin=True)
    DBManager.get_inst().session.add(testgroupuser3)

    DBManager.get_inst().commit()

    testuser1.groupusers.append(testgroupuser1)
    testgroup.groupusers.append(testgroupuser1)

    testuser2.groupusers.append(testgroupuser2)
    testgroup.groupusers.append(testgroupuser2)

    testuser3.groupusers.append(testgroupuser3)
    testgroup.groupusers.append(testgroupuser3)

    DBManager.get_inst().commit()
