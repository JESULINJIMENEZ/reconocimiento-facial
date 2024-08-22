import face_recognition

def detect_faces(image):
    face_locations = face_recognition.face_locations(image)
    return face_locations
