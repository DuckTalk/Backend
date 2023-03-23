from flask import request, current_app as app

from custom_logger import CustomLogger
logger = CustomLogger().setup()

@app.route('/api/user', methods=['GET', 'POST', 'DELETE'])
def handle_user():
    return {"text": f"{request.method} /api/user"}
