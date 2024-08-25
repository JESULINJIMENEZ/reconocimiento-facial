import cv2
import face_recognition
from api.utils.database import load_encodings, save_encodings

# Tamaño mínimo y máximo del rostro en píxeles para el registro
MIN_FACE_SIZE = 100  # Este valor puede ajustarse según tus pruebas
MAX_FACE_SIZE = 300  # Este valor puede ajustarse según tus pruebas

def register_user(name):
    video_capture = cv2.VideoCapture(0)
    
    print("Presiona 's' para capturar la imagen.")
    
    while True:
        ret, frame = video_capture.read()
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_frame)

        if len(face_locations) == 1:
            top, right, bottom, left = face_locations[0]
            face_width = right - left
            face_height = bottom - top

            # Comprobar si el rostro está dentro del rango de tamaño deseado
            if MIN_FACE_SIZE <= face_width <= MAX_FACE_SIZE and MIN_FACE_SIZE <= face_height <= MAX_FACE_SIZE:
                # Mostrar la imagen en una ventana
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                cv2.imshow('Registro', frame)

                # Esperar a que se presione la tecla 's' para capturar la imagen
                if cv2.waitKey(1) & 0xFF == ord('s'):
                    face_encoding = face_recognition.face_encodings(rgb_frame, [face_locations[0]])[0]

                    # Cargar encodings existentes
                    known_encodings = load_encodings()

                    # Agregar el nuevo usuario
                    known_encodings[name] = face_encoding.tolist()

                    # Guardar el archivo de encodings actualizado
                    save_encodings(known_encodings)

                    print(f"Usuario {name} registrado exitosamente.")
                    break
            else:
                print(f"El rostro no está a la distancia adecuada. Acércate o aléjate.")
        else:
            print("Asegúrate de que solo un rostro esté visible.")

        # Mostrar la imagen sin el rectángulo en la ventana
        cv2.imshow('Registro', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    video_capture.release()
    cv2.destroyAllWindows()
