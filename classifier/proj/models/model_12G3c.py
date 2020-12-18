import numpy as np
import torch
import torch.nn as nn
from torchvision.models import GoogLeNet

from .model_base import ModelBase


ID_TO_CLASSES = {
    0: "brown_spot",
    1: "healthy",
    2: "leaf_blast"
}

ID_TO_RUS = {
    0: "Бурая пятнистость",
    1: "Здоровое",
    2: "Пирикуляриоз"
}


class Model12G3c(ModelBase):
    """
    Model trained on 12G Kaggle dataset:
    https://www.kaggle.com/minhhuy2810/rice-diseases-image-dataset
    3 classes taken (no Hispa).

    """
    def __init__(self, threshold, device, **kwargs):
        super().__init__(device, **kwargs)

        self.threshold = threshold

    @staticmethod
    def version():
        return '0.1'

    @staticmethod
    def info():
        return f"Model12G3c v{Model12G3c.version()}"

    def init(self, model_state):
        model = GoogLeNet(transform_input=True,
                          aux_logits=False,
                          init_weights=False)
        if model_state is None:
            raise Exception("ERROR: Model state has not been loaded")

        n_inputs = model.fc.in_features
        model.fc = nn.Linear(n_inputs, 3)
        model.load_state_dict(model_state)

        return model

    def predict(self, img):
        self.model.eval()

        with torch.no_grad():
            img = self.preprocess(img)
            img = img[None, :, :, :]
            preds = self.model(img.to(self.device)).detach().cpu()
            preds = preds.numpy()[0]
            preds = np.exp(preds)
            preds /= preds.sum()

            diseases = []
            for i, pred in enumerate(preds):
                if (i != 1) and (pred > self.threshold):
                    diseases.append(ID_TO_RUS[i])

            result = {
                "diseases": diseases,
                "details": {
                    ID_TO_RUS[1]: float(preds[1]),  # healthy
                    ID_TO_RUS[0]: float(preds[0]),  # brown_spot
                    ID_TO_RUS[2]: float(preds[2])   # leaf_blast
                }
            }
            return result
