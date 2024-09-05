from fastapi import FastAPI, HTTPException, File, UploadFile
from fastapi.responses import JSONResponse
from typing import Optional
import cv2
import face_recognition
import numpy as np
from api.utils.database import load_encodings, save_encodings
from api.utils.encoding import encode_faces

app = FastAPI()

# Tamaño mínimo y máximo del rostro en píxeles para el registro
MIN_FACE_SIZE = 100
MAX_FACE_SIZE = 300

@app.post("/register/")
async def register_user(name: str, frame: UploadFile = File(...)):
    # Leer la imagen enviada
    image = cv2.imdecode(np.fromstring(await frame.read(), np.uint8), cv2.IMREAD_COLOR)

    # Convertir la imagen a RGB
    rgb_frame = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Detectar rostros en la imagen
    face_locations = face_recognition.face_locations(rgb_frame)

    if len(face_locations) != 1:
        return JSONResponse(status_code=400, content={"message": "Asegúrate de que solo un rostro esté visible."})

    top, right, bottom, left = face_locations[0]
    face_width = right - left
    face_height = bottom - top

    if not (MIN_FACE_SIZE <= face_width <= MAX_FACE_SIZE and MIN_FACE_SIZE <= face_height <= MAX_FACE_SIZE):
        return JSONResponse(status_code=400, content={"message": "El rostro no está a la distancia adecuada. Acércate o aléjate."})

    # Codificar el rostro
    face_encodings = encode_faces(rgb_frame, face_locations)

    if len(face_encodings) != 1:
        return JSONResponse(status_code=400, content={"message": "No se pudo codificar el rostro."})

    # Cargar las codificaciones existentes
    encodings = load_encodings()

    # Agregar la nueva codificación
    encodings[name] = face_encodings[0].tolist()

    # Guardar las codificaciones actualizadas
    save_encodings(encodings)

    return JSONResponse(status_code=200, content={"message": "Registro exitoso"})