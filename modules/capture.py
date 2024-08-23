import cv2

# Función para capturar una imagen desde la cámara
def capture_image():
    # Inicia la captura de video desde la cámara
    video_capture = cv2.VideoCapture(0)

    while True:
        # Captura un frame de video
        ret, frame = video_capture.read()
        # Muestra el frame capturado
        cv2.imshow('Captura - Vista Previa', frame)

        # Si se presiona la tecla 's', sale del bucle y captura la imagen
        if cv2.waitKey(1) & 0xFF == ord('s'):
            break

    # Libera la cámara y cierra las ventanas de OpenCV
    video_capture.release()
    cv2.destroyAllWindows()

    # Retorna el frame capturado
    return frame
