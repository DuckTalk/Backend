from flask import request, current_app as app

from custom_logger import CustomLogger
logger = CustomLogger().setup()

@app.route('/api/token', methods=['GET', 'DELETE'])
def handle_token():
    return {"text": f"{request.method} /api/token"}
