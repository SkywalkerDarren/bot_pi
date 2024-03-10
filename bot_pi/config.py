import json
import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
CONFIG_JSON_PATH = os.path.join(PROJECT_ROOT, "config", "config.json")
MODELS_PATH = os.path.join(PROJECT_ROOT, "models")
with open(CONFIG_JSON_PATH, "r") as f:
    CONFIG = json.load(f)
