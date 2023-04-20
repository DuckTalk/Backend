from flask import request, current_app as app
import traceback

import data_classes
import response_formatter as rf
from database.db_manager import DBManager
from database.model import Base, User as Userdb, Group as Groupdb, GroupUser as GroupUserdb, \
                           Message as Messagedb
from custom_logger import CustomLogger
logger = CustomLogger().setup()

@app.route('/api/user', methods=['GET', 'POST', 'DELETE'])
def handle_user():
    try:
        payload = request.json
        if "data" not in payload.keys():
            return {"Error": "missing data"}

        if request.method == "GET":
            resp = get_user(payload["data"])
        if request.method == "POST":
            resp = post_user(payload["data"])
        if request.method == "DELETE":
            resp = delete_user(payload["data"])

        return rf.format(resp)
    except Exception:
        logger.error(traceback.format_exc())

@app.route("/api/user/<int:user_id>")
def get_user_by_id(user_id: int):
    try:
        saved_user = DBManager.get_inst().get_userdb_from_id(user_id)
        if saved_user is None:
            resp = f"User with id '{user_id}' not found"
        else:
            resp = DBManager.user_from_userdb(saved_user).to_json_obj()

        return rf.format(resp)
    except Exception as e:
        logger.error(e)

def get_user(data: dict):
    required_keys = ["user_id"]
    for key in required_keys:
        if not key in data.keys():
            return f"Missing key '{key}' in request {data}"

    saved_user = DBManager.get_inst().get_userdb_from_id(data["user_id"])
    if saved_user is None:
        return f"User with id '{data['user_id']}' not found"
    return DBManager.user_from_userdb(saved_user).to_json_obj()

def post_user(data: dict):
    required_keys = ["username", "email", "pw_hash", "salt"]
    for key in required_keys:
        if not key in data.keys():
            return f"Missing key '{key}' in request {data}"

    DBManager.get_inst().add_user(data["username"], data["email"], "some_key", data["pw_hash"], data["salt"])
    return {"user_id": DBManager.get_inst().get_userdb_from_email(data["email"]).user_id}

def delete_user(data: dict):
    saved_user = DBManager.get_inst().get_userdb_from_id(data["user_id"])
    if saved_user is None:
        return f"User with id '{data['user_id']}' not found"
    DBManager.get_inst().delete_user(saved_user.user_id)
    return {}

# test endpoints
from tests import testdata

@app.route("/api/user/test1")
def get_user_by_id_testdata1():
    try:
        testdata.create()

        resp = DBManager.user_from_userdb(testdata.testuser1).to_json_obj()

        return rf.format(resp)
    except Exception:
        logger.error(traceback.format_exc())

@app.route("/api/user/test2")
def get_user_by_id_testdata2():
    try:
        testdata.create()

        resp = DBManager.user_from_userdb(testdata.testuser2).to_json_obj()

        return rf.format(resp)
    except Exception:
        logger.error(traceback.format_exc())

@app.route("/api/user/test3")
def get_user_by_id_testdata3():
    try:
        testdata.create()

        resp = DBManager.user_from_userdb(testdata.testuser3).to_json_obj()

        return rf.format(resp)
    except Exception:
        logger.error(traceback.format_exc())
