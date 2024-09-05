import json
import os

def load_encodings(file_path='data/encodings.json'):
    if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
        return {}

    try:
        with open(file_path, 'r') as f:
            encodings = json.load(f)
    except json.JSONDecodeError:
        print("Error: El archivo de encodings está corrupto. Creando un nuevo archivo.")
        encodings = {}

    return encodings

def save_encodings(encodings, file_path='data/encodings.json'):
    with open(file_path, 'w') as f:
        json.dump(encodings, f)
