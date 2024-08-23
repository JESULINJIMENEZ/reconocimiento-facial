import numpy as np

def compare_faces(known_encodings, face_encoding):
    """Compara un encoding de rostro con los encodings conocidos y devuelve el nombre más cercano."""
    
    name = None
    min_distance = float('inf')  # Inicializar con un valor muy grande
    
    for stored_name, stored_encoding in known_encodings.items():
        stored_encoding = np.array(stored_encoding)  # Convertir la lista a numpy array
        distance = np.linalg.norm(stored_encoding - np.array(face_encoding))
        if distance < min_distance:
            min_distance = distance
            name = stored_name
    
    return name
