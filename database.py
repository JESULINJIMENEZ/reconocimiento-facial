import json
import os

def load_encodings(file_path='encodings.json'):
    # Verifica si el archivo existe y no está vacío
    if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
        # Si el archivo no existe o está vacío, devuelve un diccionario vacío
        return {}

    try:
        with open(file_path, 'r') as f:
            encodings = json.load(f)
    except json.JSONDecodeError:
        # Si ocurre un error al decodificar el JSON, devuelve un diccionario vacío
        print("Error: El archivo de encodings está corrupto. Creando un nuevo archivo.")
        encodings = {}
    
    return encodings

def save_encodings(encodings, file_path='encodings.json'):
    with open(file_path, 'w') as f:
        json.dump(encodings, f)
