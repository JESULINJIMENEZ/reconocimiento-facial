import cv2
import face_recognition
import json
from modules.database import load_encodings, save_encodings

def register_user(name):
    # Iniciar la captura de video desde la cámara
    video_capture = cv2.VideoCapture(0)
    
    print("Presiona 's' para capturar la imagen.")
    
    while True:
        # Capturar un frame de video
        ret, frame = video_capture.read()
        
        # Mostrar la imagen en una ventana
        cv2.imshow('Registro', frame)
        
        # Esperar a que se presione la tecla 's' para capturar la imagen
        if cv2.waitKey(1) & 0xFF == ord('s'):
            break
    
    # Liberar la captura de video
    video_capture.release()
    cv2.destroyAllWindows()

    # Detectar el rostro en la imagen capturada
    face_locations = face_recognition.face_locations(frame)
    if len(face_locations) != 1:
        print("Asegúrate de que solo un rostro esté visible.")
        return
    
    # Extraer el encoding del rostro
    face_encoding = face_recognition.face_encodings(frame, face_locations)[0]
    
    # Cargar encodings existentes
    known_encodings = load_encodings()

    # Agregar el nuevo usuario
    known_encodings[name] = face_encoding.tolist()
    
    # Guardar el archivo de encodings actualizado
    save_encodings(known_encodings)

    print(f"Usuario {name} registrado exitosamente.")
