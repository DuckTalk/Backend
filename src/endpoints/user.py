from flask import request, current_app as app

import data_classes
import response_formatter as rf
from database.db_manager import DBManager
from custom_logger import CustomLogger
logger = CustomLogger().setup()

@app.route('/api/user', methods=['GET', 'POST', 'DELETE'])
def handle_user():
    payload = request.json

    if request.method == "GET":
        resp = get_user(payload["data"])
    if request.method == "POST":
        resp = add_user(payload["data"])

    return rf.format(resp)

def add_user(data: dict):
    required_keys = ["username", "email", "pw_hash", "salt"]
    for key in required_keys:
        if not key in data.keys():
            return f"Missing key '{key}' in request {data}"

    DBManager.get_inst().add_user(data["username"], data["email"], "some_key", data["pw_hash"], data["salt"])
    return {}

def get_user(data: dict):
    required_keys = ["user_id"]
    for key in required_keys:
        if not key in data.keys():
            return f"Missing key '{key}' in request {data}"

    saved_user = DBManager.get_inst().get_userdb_from_id(data["user_id"])
    if saved_user is None:
        return f"User with id '{data['user_id']}' not found"
    return data_classes.User.from_userdb(saved_user).to_json_obj()
