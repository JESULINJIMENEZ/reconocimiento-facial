import json
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import JSONResponse
from api.utils.encoding import encode_faces
from api.utils.database import load_encodings, save_encodings

app = FastAPI()

# Cargar codificaciones existentes o crear el archivo si no existe
def load_encodings(file_path='data/encodings.json'):
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}  # Si el archivo no existe o está vacío, devolvemos un diccionario vacío

# Guardar las codificaciones en el archivo JSON
def save_encodings(encodings, file_path='data/encodings.json'):
    try:
        print(f"Guardando las codificaciones en {file_path}")  # Depurar la ruta
        with open(file_path, 'w') as f:
            json.dump(encodings, f)
        print("Codificaciones guardadas correctamente")
    except Exception as e:
        print(f"Error al guardar las codificaciones: {e}")

@app.post("/register/")
async def register_user(name: str = Form(...), frame: UploadFile = File(...)):
    # Verifica si los datos están llegando
    print(f"Nombre recibido: {name}")
    print(f"Archivo recibido: {frame.filename}")
    
    # Procesar la imagen
    image_data = await frame.read()
    face_encodings = encode_faces(image_data)
    
    if len(face_encodings) != 1:
        return JSONResponse(status_code=400, content={"message": "Se detectó más de un rostro o ninguno."})

    # Cargar las codificaciones existentes
    known_encodings = load_encodings()
    
    # Agregar la nueva codificación con el nombre
    known_encodings[name] = face_encodings[0].tolist()

    # Guardar las codificaciones actualizadas
    save_encodings(known_encodings)

    return JSONResponse(content={"message": f"Usuario {name} registrado exitosamente."})
