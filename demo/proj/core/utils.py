import os
import yaml


def read_config(config_path="config.yml"):
    if not os.path.exists(config_path):
        raise Exception(f"ERROR: config file {config_path} not found")

    with open(config_path, "r") as file:
        return yaml.load(file, yaml.FullLoader)
