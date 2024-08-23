import cv2
import face_recognition
import dlib
from modules.database import load_encodings
from modules.comparison import compare_faces

# Carga los modelos de Dlib
predictor = dlib.shape_predictor('data/shape_predictor_68_face_landmarks.dat')
face_rec = dlib.face_recognition_model_v1('data/dlib_face_recognition_resnet_model_v1.dat')

def authenticate_user():
    """Autentica al usuario basado en el reconocimiento facial."""
    known_encodings = load_encodings()

    video_capture = cv2.VideoCapture(0)
    access_granted = False

    while not access_granted:
        ret, frame = video_capture.read()
        if not ret:
            print("Error al capturar la imagen.")
            continue

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_frame)

        for face_location in face_locations:
            shape = predictor(rgb_frame, dlib.rectangle(*face_location))
            face_encoding = face_rec.compute_face_descriptor(rgb_frame, shape)

            name = compare_faces(known_encodings, face_encoding)
            
            if name:
                print(f"Acceso concedido a {name}.")
                access_granted = True  # Salir del ciclo si se concede el acceso

        cv2.imshow('Video', frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video_capture.release()
    cv2.destroyAllWindows()
