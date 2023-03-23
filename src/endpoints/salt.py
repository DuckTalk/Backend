from flask import request, current_app as app

from custom_logger import CustomLogger
logger = CustomLogger().setup()

@app.route('/api/salt', methods=['GET'])
def handle_salt():
    return {"text": f"{request.method} /api/salt"}
