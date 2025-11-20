# PERCEPTION/nn_wrappers.py
"""
Lekki wrapper do integracji z modelami percepcyjnymi (vision/audio/text).
Funkcja predict(obs) -> dict raw outputs (logits/probs).
W tej warstwie możesz osadzić PyTorch/TensorFlow/onnxruntime calls.
"""

from typing import Dict, Any
import random

class DummyVisionModel:
    def predict(self, image_bytes: bytes) -> Dict[str,float]:
        # demo: zwraca prawdopodobieństwa kilku klas (mock)
        return {"cat": random.random(), "dog": random.random(), "person": random.random()}

class DummyAudioModel:
    def predict(self, audio_samples) -> Dict[str,float]:
        return {"speech": random.random(), "music": random.random()}