import cv2
import face_recognition
from api.utils.database import load_encodings, save_encodings

MIN_FACE_SIZE = 100
MAX_FACE_SIZE = 300

def register_user(name):
    video_capture = cv2.VideoCapture(0)

    while True:
        ret, frame = video_capture.read()
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_frame)

        if len(face_locations) == 1:
            top, right, bottom, left = face_locations[0]
            face_width = right - left
            face_height = bottom - top

            if MIN_FACE_SIZE <= face_width <= MAX_FACE_SIZE and MIN_FACE_SIZE <= face_height <= MAX_FACE_SIZE:
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                cv2.imshow('Registro', frame)

                if cv2.waitKey(1) & 0xFF == ord('s'):
                    face_encoding = face_recognition.face_encodings(rgb_frame, [face_locations[0]])[0]

                    known_encodings = load_encodings()
                    known_encodings[name] = face_encoding.tolist()
                    save_encodings(known_encodings)

                    print(f"Usuario {name} registrado exitosamente.")
                    break
            else:
                print(f"El rostro no está a la distancia adecuada. Acércate o aléjate.")
        else:
            print("Asegúrate de que solo un rostro esté visible.")

        cv2.imshow('Registro', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video_capture.release()
    cv2.destroyAllWindows()
