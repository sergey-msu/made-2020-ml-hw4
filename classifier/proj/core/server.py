# system
import time
from datetime import datetime as dt
import logging
from logging.handlers import TimedRotatingFileHandler

# 3rd parties
from flask import Flask

# project
from core.utils import read_config, load_model
from core.store import ImageStore


class ClassifierServer:
    def __init__(self, config_path="config.yml"):
        self.config = read_config(config_path)
        self.logger = None
        self.model = None
        self.image_store = None
        self.app = None

    def print(self, message):
        now = dt.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        print(f"{now}: {message}")

    def log(self, message, level=10):
        self.logger.log(level, message)

    def create(self):
        self.print("creating application...")

        # create logger
        try:
            log_cfg = self.config["logger"]
            log_name = log_cfg["name"]
            log_level = log_cfg["level"]

            logger = logging.getLogger(log_name)
            logger.setLevel(log_level)

            handler = TimedRotatingFileHandler(
                filename=log_cfg["path"],
                when=log_cfg["when"],
                interval=log_cfg["interval"],
                utc=True)
            handler.setLevel(log_level)
            formatter = logging.Formatter('%(asctime)s [%(levelname)s] > %(message)s')
            formatter.converter = time.gmtime
            handler.setFormatter(formatter)
            logger.addHandler(handler)

            self.print("logger: OK")
            self.logger = logger
        except Exception:
            self.print("logger: FAILED")
            raise

        # create Flask app
        try:
            app_cfg = self.config["app"]
            name = app_cfg["name"]
            app = Flask(name)
            app.logger.disabled = True
            logging.getLogger('werkzeug').disabled = True

            self.print("flask: OK")
            self.app = app
        except Exception:
            self.print("flask: FAILED")
            raise

        # create classification model
        try:
            model_name = app_cfg["model"]
            model_cfg = self.config["models"][model_name]
            model = load_model(model_name, model_cfg, logger=self.logger)

            self.print("model: OK")
            self.model = model
        except Exception:
            self.print("model: FAILED")
            raise

        # initialize image store
        try:
            image_store = ImageStore(self.config)

            self.print("image store: OK")
            self.image_store = image_store
        except Exception:
            self.print("image store: FAILED")
            raise

        self.print("application created")
        self.log("application created")
        self.log(f"working model: {model.info()}")

        return self.app

    def run(self):
        try:
            if self.app is None:
                raise Exception("ERROR: create server first")

            app_cfg = self.config["app"]
            host = app_cfg["host"]
            port = app_cfg["port"]
            debug = app_cfg["debug"]

            self.app.run(host=host, port=port, debug=debug)
            self.log("application finished")
        except Exception:
            self.print("application starting: FAILED")
            self.log("application starting: FAILED")
            raise

    def process(self, uid, image):
        # put to store + log(ts, userid, image.size, project, uid, path)
        # classify + log(ts[=store.ts], project, uid, model_name, model_version, label)

        return self.model.predict(image)
