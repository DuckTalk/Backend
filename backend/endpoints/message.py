from flask import request, current_app as app

from custom_logger import CustomLogger
logger = CustomLogger().setup()

@app.route('/api/message', methods=['GET', 'POST', 'DELETE'])
def handle_message():
    return {"text": f"{request.method} /api/message"}
