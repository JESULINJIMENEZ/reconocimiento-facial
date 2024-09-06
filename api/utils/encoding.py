import face_recognition
from io import BytesIO
from PIL import Image

def encode_faces(image_data):
    # Convertir los datos de la imagen (bytes) en un objeto de archivo temporal
    image = Image.open(BytesIO(image_data))
    
    # Convertir la imagen al formato necesario para face_recognition
    image = face_recognition.load_image_file(BytesIO(image_data))
    
    # Detectar ubicaciones de los rostros en la imagen
    face_locations = face_recognition.face_locations(image)
    
    # Codificar los rostros encontrados
    face_encodings = face_recognition.face_encodings(image, face_locations)
    
    return face_encodings
