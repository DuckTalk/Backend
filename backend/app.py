"""Module to start a webservice to interact with the user"""
from flask import Flask

from custom_logger import CustomLogger
logger = CustomLogger().setup()

app = None

def setup():
    """Setup flask app"""

    global app
    app = Flask(__name__)
    app.app_context().push()

    logger.info("Loading endpoints")
    from endpoints import salt, token, message, user, group

    logger.info("Server started")

def run():
    """runs the app"""

    app.run(debug=False, host='0.0.0.0', port=2006)

if __name__ == "__main__":
    setup()
    run()
