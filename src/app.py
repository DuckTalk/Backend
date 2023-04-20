"""Module to start a webservice to interact with the user"""
import argparse
import json
import os

from flask import Flask

from database.db_manager import DBManager
from custom_logger import CustomLogger
logger = CustomLogger().setup()

def read_config():
    """Load the config"""

    logger.info("Loading config")

    default_conf = {
        "port": 2006,
        "debug": False
    }

    if not os.path.isfile("config.json"):
        logger.info("No config.json file found, creating a new one")
        with open("config.json", "w+") as f:
            json.dump(default_conf, f, indent=4)
        return default_conf

    with open("config.json", "r") as f:
        saved_conf = json.load(f)
    
    for key, value in saved_conf.items():
        if key in default_conf.keys():
            default_conf[key] = value
        else:
            logger.warning(f"Unknown key '{key}' found in config.json")

    return default_conf

def parse_args(in_args: dict | None = None):
    """Read the commandline args"""

    parser = argparse.ArgumentParser(prog="DuckTalk_backend")
    parser.add_argument("--port", type=str, required=False)
    parser.add_argument("-p", type=str, required=False)
    parser.add_argument("--dbfile", type=str, required=False)
    if in_args is None:
        args = vars(parser.parse_args())
    else:
        args = vars(parser.parse_args(in_args))

    config = read_config()

    if args["port"] is not None:
        config["port"] = args["port"]
    if args["p"] is not None:
        config["port"] = args["p"]
    if args["dbfile"] is not None:
        config["dbfile"] = args["dbfile"]

    return config

def setup(args: dict):
    """Setup flask app"""

    app = Flask(__name__)
    app.app_context().push()

    logger.info("Loading endpoints")
    from endpoints import salt, token, message, user, group, home
    
    if "dbfile" in args.keys():
        DBManager._dbfile = args["dbfile"]
    DBManager()

    logger.info("Server started")
    return app

def run(app: Flask, config):
    """runs the app"""

    app.run(debug=config["debug"], host='0.0.0.0', port=config["port"])

def run_app(in_args):
    logger.info("--------------------------------")
    logger.info("Starting server...")
    args = parse_args(in_args)
    app = setup(args)
    run(app, args)

if __name__ == "__main__":
    run_app(None)
