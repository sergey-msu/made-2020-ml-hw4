import requests
from flask import Flask
from flask_login import LoginManager
from core.utils import read_config
from core.user import DemoUser


class DemoServer:
    def __init__(self, config_path="config.yml"):
        self.config = read_config(config_path)
        self.classifier_url = None
        self.login_manager = None
        self.app = None

    def create(self):
        # create Flask app
        app_cfg = self.config["app"]
        name = app_cfg["name"]
        template_dir = app_cfg["template_dir"]
        static_dir = app_cfg["static_dir"]

        self.app = Flask(name,
                         template_folder=template_dir,
                         static_folder=static_dir)

        # create login manager with single demo user
        self.app.config["SECRET_KEY"] = self.__get_secret("secret")
        login_manager = LoginManager()
        login_manager.init_app(self.app)
        login_manager.login_view = "login"

        @login_manager.user_loader
        def load_user(uid):
            return self.get_user_by_id(uid)

        self.login_manager = login_manager

        # create classifier url
        classifier_cfg = self.config["classifier"]
        classifier_host = classifier_cfg["host"]
        classifier_port = classifier_cfg["port"]
        classifier_endpoint = classifier_cfg["endpoint"]

        self.classifier_url = f"http://{classifier_host}:{classifier_port}/{classifier_endpoint}"

        return self.app

    def run(self):
        if self.app is None:
            raise Exception("ERROR: create server first")

        app_cfg = self.config["app"]
        host = app_cfg["host"]
        port = app_cfg["port"]
        debug = app_cfg["debug"]

        self.app.run(host=host, port=port, debug=debug)

    def classify(self, image):
        # put to store + log(ts, userid, image.size, project, uid, path)
        # classify + log(ts[=store.ts], project, uid, model_name, model_version, label)

        response = requests.post(self.classifier_url, files=[('img', image)])
        result = response.json()['result']

        return result

    def get_user_by_name(self, name):
        users = self.__get_secret("users")
        for user in users:
            if user["name"] == name:
                return DemoUser(user["id"], user["name"], user["password"])

        return None

    def get_user_by_id(self, uid):
        users = self.__get_secret("users")
        for user in users:
            if str(user["id"]) == uid:
                return DemoUser(user["id"], user["name"], user["password"])

        return None

    def __get_secret(self, key):
        secret_path = self.config["app"]["secret_path"]
        return read_config(secret_path)["demo"][key]
