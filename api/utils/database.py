import json

def load_encodings(file_path='data/encodings.json'):
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_encodings(encodings, file_path='data/encodings.json'):
    try:
        with open(file_path, 'w') as f:
            json.dump(encodings, f)
        print("Codificaciones guardadas correctamente")
    except Exception as e:
        print(f"Error al guardar las codificaciones: {e}")
