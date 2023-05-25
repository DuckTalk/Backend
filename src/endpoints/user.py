from flask import request, current_app as app
import traceback

import data_classes
import response_formatter as rf
from database.db_manager import DBManager
from database.model import Base, User as Userdb, Group as Groupdb, GroupUser as GroupUserdb, \
                           Message as Messagedb
from custom_logger import CustomLogger
logger = CustomLogger().setup()

@app.route('/api/user', methods=['POST'])
def handle_user():
    try:
        payload = request.json
        if "data" not in payload.keys():
            return {"Error": "missing data"}

        if request.method == "POST":
            resp = post_user(payload["data"])

        return rf.format(resp)
    except Exception:
        logger.error(traceback.format_exc())

@app.route("/api/user/<int:user_id>", methods=['GET', 'DELETE'])
def get_user_by_id(user_id: int):
    if request.method == "GET":
        resp = get_user(user_id)
    if request.method == "DELETE":
        resp = delete_user(user_id)

    return rf.format(resp)

@app.route("/api/user/<string:email>", methods=['GET'])
def get_user_by_email(email: str):
    user_id = DBManager.get_inst().get_userdb_from_email(email).user_id
    resp = get_user(user_id)
    return rf.format(resp)

def get_user(user_id: int):
    try:
        saved_user = DBManager.get_inst().get_userdb_from_id(user_id)
        if saved_user is None:
            resp = f"User with id '{user_id}' not found"
        else:
            resp = DBManager.user_from_userdb(saved_user).to_json_obj()
        return resp
    except Exception as e:
        logger.error(e)

def post_user(data: dict):
    required_keys = ["username", "email", "pw_hash", "salt"]
    for key in required_keys:
        if not key in data.keys():
            return f"Missing key '{key}'"

    DBManager.get_inst().add_user(data["username"], data["email"], "some_key", data["pw_hash"], data["salt"])
    return {"user_id": DBManager.get_inst().get_userdb_from_email(data["email"]).user_id}

def delete_user(user_id: int):
    saved_user = DBManager.get_inst().get_userdb_from_id(user_id)
    if saved_user is None:
        return f"User with id '{user_id}' not found"
    DBManager.get_inst().delete_user(saved_user.user_id)
    return {}

# test endpoints
from tests import testdata

@app.route("/api/user/test1")
def get_user_by_id_testdata1():
    try:
        resp = DBManager.user_from_userdb(testdata.testuser1).to_json_obj()

        return rf.format(resp)
    except Exception:
        logger.error(traceback.format_exc())

@app.route("/api/user/test2")
def get_user_by_id_testdata2():
    try:
        resp = DBManager.user_from_userdb(testdata.testuser2).to_json_obj()

        return rf.format(resp)
    except Exception:
        logger.error(traceback.format_exc())

@app.route("/api/user/test3")
def get_user_by_id_testdata3():
    try:
        resp = DBManager.user_from_userdb(testdata.testuser3).to_json_obj()

        return rf.format(resp)
    except Exception:
        logger.error(traceback.format_exc())
