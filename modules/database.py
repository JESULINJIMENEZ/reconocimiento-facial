# modules/database.py

import json
import os

ENCODINGS_FILE = 'data/encodings.json'

def load_encodings():
    """Carga los encodings desde el archivo JSON"""
    if os.path.exists(ENCODINGS_FILE):
        with open(ENCODINGS_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_encodings(encodings):
    """Guarda los encodings en el archivo JSON"""
    with open(ENCODINGS_FILE, 'w') as f:
        json.dump(encodings, f)
