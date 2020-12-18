import os
import torch


class ModelBase:
    def __init__(self, device, logger, **kwargs):
        self.logger = logger
        self.preprocess = None
        self.model = None

        if device.lower() == 'gpu':
            avail = torch.cuda.is_available()
            if not avail:
                raise Exception('ERROR: unable to run model on GPU')
            device = torch.cuda.current_device()

        self.device = device

        self.logger.log(10, f'model is running on device: {device}')

    @staticmethod
    def version():
        raise Exception('ERROR: version not implemented')

    @staticmethod
    def info():
        raise Exception('ERROR: info not implemented')

    def load(self, file_path):
        if not os.path.exists(file_path):
            raise Exception(f'ERROR: File "{file_path}" not exists')

        map_location = torch.device('cpu') if self.device == 'cpu' else None
        state = torch.load(file_path, map_location=map_location)
        state_version = state['version']
        script_version = self.version()

        if state_version != script_version:
            raise Exception(f'ERROR: Current script version is {script_version} but loaded is {state_version}')

        model_state = state['model_state']
        preprocess = state["preprocess"]

        self.preprocess = preprocess
        self.model = self.init(model_state)

    def init(self, model_state):
        raise Exception('ERROR: init not implemented')

    def train(self):
        pass

    def predict(self, img):
        raise Exception('ERROR: predictions not implemented')
