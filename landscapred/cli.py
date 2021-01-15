import pkgutil
from tempfile import NamedTemporaryFile
from typing import Any

import cv2
from flask import Flask, request
from numpy import argmax
from requests import get as requests_get
from tensorflow.keras.models import load_model


app = Flask(__name__)


with NamedTemporaryFile("r+b") as fh:
    fh.write(pkgutil.get_data("landscapred", "model.h5"))
    fh.seek(0)
    model = load_model(fh.name)
label_names = ["buildings", "forest", "glacier", "mountain", "sea", "street"]


@app.route("/", methods=["POST"])
def predict() -> Any:
    content = request.get_json()
    url = content["url"]
    response = requests_get(url)
    with NamedTemporaryFile("wb", delete=False) as fh:
        fh.write(response.content)
    image = cv2.imread(fh.name)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = cv2.resize(image, (150, 150))
    probas = model.predict(image[None, ...])[0]
    return dict(
        max=label_names[argmax(probas)],
        probas={label: float(proba) for label, proba in zip(label_names, probas)},
    )


def main() -> None:
    app.run("0.0.0.0", port=5000)
