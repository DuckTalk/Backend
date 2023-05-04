from flask import request, current_app as app

import data_classes
import response_formatter as rf
from database.db_manager import DBManager
from database.model import Base, User as Userdb, Group as Groupdb, GroupUser as GroupUserdb, \
                           Message as Messagedb
from custom_logger import CustomLogger
logger = CustomLogger().setup()

@app.route('/api/message', methods=['POST'])
def handle_message():
    try:
        payload = request.json
        if "data" not in payload.keys():
            return rf.format(f"Missing key 'data'")

        return rf.format(post_message(payload["data"]))
    except Exception as e:
        logger.error(e)

@app.route('/api/message/<int:message_id>', methods=['GET'])
def get_message_by_id(message_id: dict):
    try:
        saved_message = DBManager.get_inst().get_messagedb_from_id(message_id)
        if saved_message is None:
            resp = f"Message with id '{message_id}' not found"
        else:
            resp = DBManager.message_from_messagedb(saved_message).to_json_obj()

        return rf.format(resp)
    except Exception as e:
        logger.error(e)

def post_message(data: dict):
    required_keys = ["sender_id", "receiver", "content"]
    for key in required_keys:
        if not key in data.keys():
            return f"Missing key '{key}'"
    
    if not "type" in data["receiver"].keys():
        return "Missing key 'type'"

    if data["receiver"]["type"] == "group":
        if not "group_id" in data["receiver"].keys():
            return "Missing key 'group_id'"

        return _post_gm(data)
    else:
        if not "user_id" in data["receiver"].keys():
            return "Missing key 'user_id'"

        return _post_pm(data)

def _post_gm(data: dict):
    DBManager.get_inst().add_message(data["content"], data["sender_id"], data["receiver"]["group_id"])

def _post_pm(data: dict):
    stored_sender = DBManager.get_inst().get_userdb_from_id(data["sender_id"])
    if stored_sender is None:
        return f"User with user_id {data['sender_id']} not found"
    stored_receiver = DBManager.get_inst().get_userdb_from_id(data["receiver"]["user_id"])
    if stored_receiver is None:
        return f"User with user_id {data['receiver']['user_id']} not found"

    # find private chat group
    receiver_group = None
    for groupuser in stored_receiver.groupusers:
        group: Groupdb = DBManager.get_inst().get_groupdb_from_id(groupuser.group_id)
        if group.is_privatechat and (stored_sender in group.groupusers):
            receiver_group = group

    if receiver_group is None:
        receiver_group_id = DBManager.get_inst().add_group([stored_sender, stored_receiver], True, "", "")
        receiver_group = DBManager.get_inst().get_groupdb_from_id(receiver_group_id)

    message_id = DBManager.get_inst().add_message(data["content"], data["sender_id"], receiver_group.group_id)

    return {"message_id": message_id}

# test endpoints
from tests import testdata

@app.route("/api/message/test1")
def get_message_by_id_testdata1():
    try:
        testdata.create()

        resp = DBManager.message_from_messagedb(testdata.testmsg1).to_json_obj()

        return rf.format(resp)
    except Exception as e:
        logger.error(e)

@app.route("/api/message/test2")
def get_message_by_id_testdata2():
    try:
        testdata.create()

        resp = DBManager.message_from_messagedb(testdata.testmsg2).to_json_obj()

        return rf.format(resp)
    except Exception as e:
        logger.error(e)

@app.route("/api/message/test3")
def get_message_by_id_testdata3():
    try:
        testdata.create()

        resp = DBManager.message_from_messagedb(testdata.testmsg3).to_json_obj()

        return rf.format(resp)
    except Exception as e:
        logger.error(e)

@app.route("/api/message/test4")
def get_message_by_id_testdata4():
    try:
        testdata.create()

        resp = DBManager.message_from_messagedb(testdata.testmsg4).to_json_obj()

        return rf.format(resp)
    except Exception as e:
        logger.error(e)
