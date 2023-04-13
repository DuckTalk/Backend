from flask import request, current_app as app

from custom_logger import CustomLogger
logger = CustomLogger().setup()

@app.route('/api/home', methods=['GET'])
def handle_home():
    return "AbiAPI home page"
