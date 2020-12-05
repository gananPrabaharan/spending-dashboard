from os.path import dirname, join
import json


PROJECT_PATH = dirname(dirname(__file__))

config_file_path = join(PROJECT_PATH, 'config.json')
with open(config_file_path) as json_file:
    config = json.load(json_file)


class Paths:
    FLASK_APP = join(PROJECT_PATH, "flask_app")
    REACT_APP = join(PROJECT_PATH, "react_app")


class Deployment:
    HOST = config.get("Deployment").get("HOST")
    FLASK_PORT = config.get("Deployment").get("FLASK_PORT")
    REACT_PORT = config.get("Deployment").get("NGINX_PORT")

