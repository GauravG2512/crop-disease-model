"""
predict.py
----------
Handles model loading and image inference.
Completely decoupled from UI — no Streamlit imports here.
"""

from __future__ import annotations

import os
import numpy as np
from PIL import Image


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
MODEL_PATH       = "crop_disease_model.keras"
CLASS_NAMES_PATH = "class_names.txt"
IMAGE_SIZE       = (224, 224)
TOP_K            = 3


# ---------------------------------------------------------------------------
# Loader helpers
# ---------------------------------------------------------------------------

def load_model(path: str = MODEL_PATH):
    """
    Load a Keras .keras model file.
    Returns (model, error_string).  error_string is None on success.
    """
    if not os.path.exists(path):
        return None, (
            f"Model file `{path}` was not found.\n"
            "Place `crop_disease_model.keras` in the same directory as `app.py`."
        )
    try:
        import tensorflow as tf  # lazy import so predict.py can be imported without TF
        model = tf.keras.models.load_model(path)
        return model, None
    except ImportError:
        return None, "TensorFlow is not installed.  Run:  pip install tensorflow"
    except Exception as exc:
        return None, f"Failed to load model: {exc}"


def load_class_names(path: str = CLASS_NAMES_PATH) -> tuple[list[str] | None, str | None]:
    """
    Read class_names.txt — one class per line.
    Returns (class_names_list, error_string).
    """
    if not os.path.exists(path):
        return None, (
            f"Class names file `{path}` was not found.\n"
            "Place `class_names.txt` in the same directory as `app.py`."
        )
    with open(path, "r") as fh:
        names = [line.strip() for line in fh if line.strip()]
    if not names:
        return None, f"`{path}` exists but is empty."
    return names, None


# ---------------------------------------------------------------------------
# Preprocessing
# ---------------------------------------------------------------------------

def preprocess(image: Image.Image) -> "np.ndarray":
    """
    Resize PIL image to (224, 224), normalise to [0, 1], add batch dim.
    Matches training preprocessing:  tf.keras.layers.Rescaling(1./255)
    """
    img = image.resize(IMAGE_SIZE, Image.LANCZOS)
    arr = np.array(img, dtype=np.float32)
    # No normalisation here — model contains Rescaling(1./255) internally
    arr = np.expand_dims(arr, axis=0)   # shape: (1, 224, 224, 3)
    return arr


# ---------------------------------------------------------------------------
# Inference
# ---------------------------------------------------------------------------

def predict(model, image: Image.Image, class_names: list[str]) -> dict:
    """
    Run inference and return a results dict:
    {
        "predicted_class": str,          # raw class name
        "confidence": float,             # 0–100
        "top_k": [                       # top-K predictions
            {"class": str, "confidence": float}, ...
        ]
    }
    """
    arr = preprocess(image)
    raw = model.predict(arr, verbose=0)[0]   # shape: (num_classes,)

    predicted_idx   = int(np.argmax(raw))
    confidence      = float(raw[predicted_idx]) * 100
    predicted_class = class_names[predicted_idx]

    top_k_idx = np.argsort(raw)[::-1][:TOP_K]
    top_k = [
        {
            "class":      class_names[i] if i < len(class_names) else f"Class {i}",
            "confidence": float(raw[i]) * 100,
        }
        for i in top_k_idx
    ]

    return {
        "predicted_class": predicted_class,
        "confidence":      confidence,
        "top_k":           top_k,
    }