import cv2
import dlib
import numpy as np
from api.utils.database import load_encodings

# Cargar los modelos de dlib
predictor = dlib.shape_predictor('data/shape_predictor_68_face_landmarks.dat')
face_rec = dlib.face_recognition_model_v1('data/dlib_face_recognition_resnet_model_v1.dat')

# Parámetros de distancia
MIN_FACE_SIZE = 100  # Tamaño mínimo de la cara en píxeles (umbral inferior)
MAX_FACE_SIZE = 300  # Tamaño máximo de la cara en píxeles (umbral superior)

def authenticate_user():
    # Cargar las codificaciones conocidas
    known_encodings = load_encodings()

    # Iniciar la cámara
    video_capture = cv2.VideoCapture(0)
    window_name = 'Autenticación Facial'
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)

    authenticated = False

    while True:
        # Capturar un frame de la cámara
        ret, frame = video_capture.read()

        # Convertir la imagen de BGR (que usa OpenCV) a RGB (que usa dlib)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Localizar caras en el frame
        face_locations = dlib.get_frontal_face_detector()(rgb_frame, 1)

        # Intentar autenticar a cada cara detectada
        for face_location in face_locations:
            # Calcular el tamaño de la cara
            face_width = face_location.right() - face_location.left()
            face_height = face_location.bottom() - face_location.top()
            face_size = max(face_width, face_height)

            # Verificar si el tamaño de la cara está dentro del rango deseado
            if MIN_FACE_SIZE <= face_size <= MAX_FACE_SIZE:
                shape = predictor(rgb_frame, face_location)
                face_encoding = np.array(face_rec.compute_face_descriptor(rgb_frame, shape))

                for name, known_encoding in known_encodings.items():
                    match = np.linalg.norm([known_encoding] - face_encoding, axis=1) < 0.6
                    if match[0]:
                        print(f"Acceso concedido a {name}.")
                        cv2.putText(frame, f"Acceso concedido a {name}", (face_location.left(), face_location.top() - 10),
                                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
                        authenticated = True
                        break
                else:
                    print("Acceso denegado.")
                    cv2.putText(frame, "Acceso denegado", (face_location.left(), face_location.top() - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
            else:
                print("Rostro fuera del rango de distancia.")
                cv2.putText(frame, "Fuera de rango", (face_location.left(), face_location.top() - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)

            # Mostrar el cuadro alrededor del rostro y el nombre
            top, right, bottom, left = (face_location.top(), face_location.right(),
                                        face_location.bottom(), face_location.left())
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

        cv2.imshow(window_name, frame)

        if authenticated or cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Liberar la cámara y cerrar la ventana
    video_capture.release()
    cv2.destroyAllWindows()
