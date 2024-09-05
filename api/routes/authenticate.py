from fastapi import FastAPI, HTTPException, Depends
import cv2
import dlib
import numpy as np
from typing import Optional
from api.utils.database import load_encodings
from fastapi.security.oauth2 import OAuth2PasswordBearer

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

# Cargar los modelos de dlib
predictor = dlib.shape_predictor('data/shape_predictor_68_face_landmarks.dat')
face_rec = dlib.face_recognition_model_v1('data/dlib_face_recognition_resnet_model_v1.dat')

@app.post("/auth/token")
async def authenticate_user(token: Optional[str] = None):
    # Cargar las codificaciones conocidas
    known_encodings = load_encodings()

    if token is not None:
        # Verificar el token de autenticación
        pass  # Aquí iría la lógica de validación del token

    else:
        raise HTTPException(status_code=401, detail="No authorization credentials provided")

    # Iniciar la cámara
    video_capture = cv2.VideoCapture(0)

    authenticated = False

    while True:
        ret, frame = video_capture.read()

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_locations = dlib.get_frontal_face_detector()(rgb_frame, 1)

        for face_location in face_locations:
            # Calcular el tamaño de la cara
            face_width = face_location.right() - face_location.left()
            face_height = face_location.bottom() - face_location.top()
            face_size = max(face_width, face_height)

            if MIN_FACE_SIZE <= face_size <= MAX_FACE_SIZE:
                shape = predictor(rgb_frame, face_location)
                face_encoding = np.array(face_rec.compute_face_descriptor(rgb_frame, shape))

                for name, known_encoding in known_encodings.items():
                    match = np.linalg.norm([known_encoding] - face_encoding, axis=1) < 0.6
                    if match:
                        authenticated = True
                        break

        # Verificar si el usuario ha sido autenticado
        if not authenticated:
            raise HTTPException(status_code=401, detail="Authentication failed")

    video_capture.release()