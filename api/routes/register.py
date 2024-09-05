from fastapi import FastAPI, HTTPException
import cv2
import face_recognition
from typing import Optional

app = FastAPI()

# Tamaño mínimo y máximo del rostro en píxeles para el registro
MIN_FACE_SIZE = 100
MAX_FACE_SIZE = 300

@app.post("/register/")
async def register_user(name: str):
    video_capture = cv2.VideoCapture(0)

    while True:
        ret, frame = video_capture.read()
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_frame)

        if len(face_locations) == 1:
            top, right, bottom, left = face_locations
            face_width = right - left
            face_height = bottom - top

            if MIN_FACE_SIZE <= face_width <= MAX_FACE_SIZE and MIN_FACE_SIZE <= face_height <= MAX_FACE_SIZE:
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                cv2.imshow('Registro', frame)

                if cv2.waitKey(1) & 0xFF == ord('s'):
                    break
            else:
                print(f"El rostro no está a la distancia adecuada. Acércate o aléjate.")
        else:
            print("Asegúrate de que solo un rostro esté visible.")

    cv2.destroyAllWindows()