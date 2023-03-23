from flask import request, current_app as app

from custom_logger import CustomLogger
logger = CustomLogger().setup()

@app.route('/api/group', methods=['GET', 'POST', 'DELETE'])
def handle_group():
    return {"text": f"{request.method} /api/group"}
