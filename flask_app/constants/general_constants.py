from os.path import dirname, join
import json


PROJECT_PATH = dirname(dirname(dirname(__file__)))

config_file_path = join(PROJECT_PATH, 'config.json')
with open(config_file_path) as json_file:
    config = json.load(json_file)


class Paths:
    FLASK_APP = join(PROJECT_PATH, "flask_app")
    REACT_APP = join(PROJECT_PATH, "react_app")
    DATABASE = join(FLASK_APP, "database")
    RESOURCES = join(FLASK_APP, "resources")


class Files:
    CANADA_CITIES = join(Paths.RESOURCES, config.get("Files").get("CANADA_CITIES"))


class Deployment:
    HOST = config.get("Deployment").get("HOST")
    FLASK_PORT = config.get("Deployment").get("FLASK_PORT")
    REACT_PORT = config.get("Deployment").get("NGINX_PORT")


class Database:
    CONNECTION = join(Paths.FLASK_APP, config.get("DB").get("CONNECTION"))


class Columns:
    TRANSACTION_ID = "id"
    DATE = "date"
    DESCRIPTION = "description"
    WITHDRAWAL = "withdrawal"
    DEPOSIT = "deposit"
    AMOUNT = "amount"
    ACCOUNT = "account"
    CATEGORY = "category"
    VENDOR_ID = "vendorId"


class Categories:
    GROCERY = "grocery"
    GAS = "gas"
    RESTAURANTS = "restaurants"
    EDUCATION = "education"
    UTILITIES = "utilities"
    RETAIL = "retail"


class Classification:
    MIN_DISTANCE = 0.7
    NUM_NEIGHBOURS = 10
