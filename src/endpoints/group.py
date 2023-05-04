from flask import request, current_app as app
import traceback

import data_classes
import response_formatter as rf
from database.db_manager import DBManager
from database.model import Base, User as Userdb, Group as Groupdb, GroupUser as GroupUserdb, \
                           Message as Messagedb
from custom_logger import CustomLogger
logger = CustomLogger().setup()

@app.route('/api/group', methods=['POST'])
def handle_group():
    try:
        payload = request.json
        if "data" not in payload.keys():
            return rf.format(f"Missing key 'data'")

        return rf.format(post_group(payload["data"]))
    except Exception as e:
        logger.error(e)

@app.route('/api/group/<int:group_id>', methods=['GET'])
def get_group_by_id(group_id: dict):
    try:
        saved_group = DBManager.get_inst().get_groupdb_from_id(group_id)
        if saved_group is None:
            resp = f"Message with id '{group_id}' not found"
        else:
            resp = DBManager.group_from_groupdb(saved_group).to_json_obj()

        return rf.format(resp)
    except Exception as e:
        logger.error(e)

def post_group(data: dict):
    required_keys = ["groupname", "description", "user_id"]
    for key in required_keys:
        if not key in data.keys():
            return f"Missing key '{key}'"
    
    stored_user = DBManager.get_inst().get_userdb_from_id(data["user_id"])
    if stored_user is None:
        return f"User with user_id {data['user_id']} not found"

    group_id = DBManager.get_inst().add_group([stored_user], False, data["groupname"], data["description"])
    return {"group_id": group_id}

# test endpoints
from tests import testdata

@app.route('/api/group/test')
def get_group_by_id_testdata():
    try:
        testdata.create()

        resp = DBManager.group_from_groupdb(testdata.testgroup).to_json_obj()

        return rf.format(resp)
    except Exception:
        logger.error(traceback.format_exc())
