from flask import request, current_app as app

import data_classes
import response_formatter as rf
from database.db_manager import DBManager
from database.model import Base, User as Userdb, Group as Groupdb, GroupUser as GroupUserdb, \
                           Message as Messagedb
from custom_logger import CustomLogger
logger = CustomLogger().setup()

@app.route('/api/message', methods=['GET', 'POST', 'DELETE'])
def handle_message():
    payload = request.json
    if "data" not in payload.keys():
        return {"Error": "missing data"}

    if request.method == "GET":
        resp = get_message(payload["data"])
    if request.method == "POST":
        resp = post_message(payload["data"], payload["auth"])
    if request.method == "DELETE":
        resp = delete_message(payload["data"])

    return rf.format(resp)

def get_message(data: dict):
    required_keys = ["message_id"]
    for key in required_keys:
        if not key in data.keys():
            return f"Missing key '{key}' in request {data}"

def post_message(data: dict, auth: dict):
    required_keys = ["receiver", "content"]
    for key in required_keys:
        if not key in data.keys():
            return f"Missing key '{key}' in request {data}"

def delete_message(data: dict):
    required_keys = ["message_id"]
    for key in required_keys:
        if not key in data.keys():
            return f"Missing key '{key}' in request {data}"

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
