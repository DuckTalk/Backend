from flask import request, current_app as app
import traceback

import data_classes
import response_formatter as rf
from database.db_manager import DBManager
from database.model import Base, User as Userdb, Group as Groupdb, GroupUser as GroupUserdb, \
                           Message as Messagedb
from custom_logger import CustomLogger
logger = CustomLogger().setup()

@app.route('/api/group', methods=['GET', 'POST', 'DELETE'])
def handle_group():
    return {"text": f"{request.method} /api/group"}

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
