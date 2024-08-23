import json 
# Función para guardar encodings de un usuario en un archivo JSON
def save_encodings(name, encoding):
    encodings = load_encodings()

    # Agrega el encoding del nuevo usuario al diccionario existente
    encodings[name] = encoding

    # Escribe los encodings actualizados de vuelta al archivo JSON
    with open('encodings.json', 'w') as f:
        json.dump(encodings, f)

# Función para cargar encodings desde un archivo JSON
def load_encodings():
    try:
        # Intenta abrir y leer el archivo de encodings
        with open('encodings.json', 'r') as f:
            encodings = json.load(f)
        return encodings
    except FileNotFoundError:
        # Si el archivo no existe, devuelve un diccionario vacío
        return {}
