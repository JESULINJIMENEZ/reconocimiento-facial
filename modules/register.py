# modules/register.py

import cv2
import face_recognition
import os
from modules.database import save_encodings, load_encodings

def register_user(name):
    """Registra un nuevo usuario"""
    encodings = load_encodings()

    # Capturar imagen de la cámara
    video_capture = cv2.VideoCapture(0)
    while True:
        ret, frame = video_capture.read()
        cv2.imshow('Video', frame)
        
        # Esperar a que se presione la tecla 's' para capturar la imagen
        if cv2.waitKey(1) & 0xFF == ord('s'):
            break
    
    video_capture.release()
    cv2.destroyAllWindows()

    # Obtener los encodings de la imagen capturada
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    face_encodings = face_recognition.face_encodings(rgb_frame)

    if face_encodings:
        encodings[name] = face_encodings[0].tolist()
        save_encodings(encodings)
        print(f"Usuario {name} registrado con éxito.")
    else:
        print("No se detectó ningún rostro. Registro fallido.")
