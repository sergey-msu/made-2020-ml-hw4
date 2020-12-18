import os
import yaml
from models.model_12G3c import Model12G3c


def read_config(config_path="config.yml"):
    if not os.path.exists(config_path):
        raise Exception(f"ERROR: config file {config_path} not found")

    with open(config_path, "r") as file:
        return yaml.load(file, yaml.FullLoader)


def load_model(model_name, config, **kwargs):
    device = config["device"]
    file_path = get_secret('models')[model_name]
    threshold = config["threshold"]

    if model_name == "model_12G3c":
        model = Model12G3c(threshold=threshold, device=device, **kwargs)
        model.load(file_path)
        return model

    raise Exception(f"ERROR: unknown model '{model_name}'")


def get_secret(key, config_path="config.yml"):
    config = read_config(config_path)
    secret_path = config["app"]["secret_path"]
    return read_config(secret_path)["classifier"][key]
