"""Module to start a webservice to interact with the user"""
import flask
from flask import Flask, request

from custom_logger import CustomLogger

app = Flask(__name__)

"""Lets the client interact with the backend, with diffrent methods"""

logger = CustomLogger().setup()
logger.info("Server started")

@app.route('/api/message', methods=['GET', 'POST'])
def handle_message():
    """handle a message"""

    if flask.request.method == 'POST':
        return post_message()
    else:
        return get_message()

def get_message():
    """return a message"""

    logger.info("Getting message!")
    return {'schools': ""}

def post_message():
    """return a message"""
    message = request.json['message']

    logger.info(f"Posting message: {message}")
    return {'schools': ""}

def run():
    """runs the app"""
    app.run(debug=False, host='0.0.0.0', port=2006)

run()
