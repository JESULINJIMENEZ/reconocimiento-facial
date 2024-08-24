import cv2
import dlib
import numpy as np
from modules.database import load_encodings

# Cargar los modelos de dlib
predictor = dlib.shape_predictor('data/shape_predictor_68_face_landmarks.dat')
face_rec = dlib.face_recognition_model_v1('data/dlib_face_recognition_resnet_model_v1.dat')

def authenticate_user():
    # Cargar las codificaciones conocidas
    known_encodings = load_encodings()

    # Iniciar la cámara
    video_capture = cv2.VideoCapture(0)

    while True:
        # Capturar un frame de la cámara
        ret, frame = video_capture.read()

        # Convertir la imagen de BGR (que usa OpenCV) a RGB (que usa dlib)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Localizar caras en el frame
        face_locations = dlib.get_frontal_face_detector()(rgb_frame, 1)

        # Intentar autenticar a cada cara detectada
        for face_location in face_locations:
            # Obtener los landmarks faciales
            shape = predictor(rgb_frame, face_location)

            # Obtener la codificación facial utilizando los landmarks
            face_encoding = np.array(face_rec.compute_face_descriptor(rgb_frame, shape))

            # Comparar con las codificaciones conocidas
            for name, known_encoding in known_encodings.items():
                match = np.linalg.norm([known_encoding] - face_encoding, axis=1) < 0.6
                if match[0]:
                    print(f"Acceso concedido a {name}.")
                    # Cerrar la cámara y salir de la función
                    video_capture.release()
                    cv2.destroyAllWindows()
                    return

        # Mostrar el video con las detecciones
        cv2.imshow('Video', frame)

        # Salir con la tecla 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Liberar la cámara y cerrar todas las ventanas
    video_capture.release()
    cv2.destroyAllWindows()
