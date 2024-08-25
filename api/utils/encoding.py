import face_recognition

def encode_faces(image, face_locations):
    face_encodings = face_recognition.face_encodings(image, face_locations)
    return face_encodings
