import cv2
import dlib
import numpy as np
from api.utils.database import load_encodings

# Cargar los modelos de dlib
predictor = dlib.shape_predictor('data/shape_predictor_68_face_landmarks.dat')
face_rec = dlib.face_recognition_model_v1('data/dlib_face_recognition_resnet_model_v1.dat')

# Parámetros de distancia
MIN_FACE_SIZE = 100
MAX_FACE_SIZE = 300

def authenticate_user():
    known_encodings = load_encodings()
    video_capture = cv2.VideoCapture(0)
    window_name = 'Autenticación Facial'
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)

    authenticated = False

    while True:
        ret, frame = video_capture.read()
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_locations = dlib.get_frontal_face_detector()(rgb_frame, 1)

        for face_location in face_locations:
            face_width = face_location.right() - face_location.left()
            face_height = face_location.bottom() - face_location.top()
            face_size = max(face_width, face_height)

            if MIN_FACE_SIZE <= face_size <= MAX_FACE_SIZE:
                shape = predictor(rgb_frame, face_location)
                face_encoding = np.array(face_rec.compute_face_descriptor(rgb_frame, shape))

                for name, known_encoding in known_encodings.items():
                    match = np.linalg.norm([known_encoding] - face_encoding, axis=1) < 0.6
                    if match[0]:
                        authenticated = True
                        break
                if authenticated:
                    break

        if authenticated or cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video_capture.release()
    cv2.destroyAllWindows()

    return authenticated
