import numpy as np

def compare_faces(known_encodings, face_encoding):
    known_encodings_list = list(known_encodings.values())
    distances = np.linalg.norm(known_encodings_list - face_encoding, axis=1)
    min_distance_index = np.argmin(distances)

    if distances[min_distance_index] < 0.6:
        return min_distance_index
    else:
        return None
