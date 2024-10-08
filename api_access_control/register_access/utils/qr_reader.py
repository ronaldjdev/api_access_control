import cv2
from pyzbar.pyzbar import decode

# Variable global para almacenar los datos del QR

def read_qr_image(path_imagen):
    """
    Lee un código QR desde una imagen y devuelve los datos decodificados.
    """
    img = cv2.imread(path_imagen)
    qrs = decode(img)
    
    for qr in qrs:
        qr_data = qr.data.decode('utf-8')
        return qr_data

    return None

# def read_qr_camera():
#     """
#     Lee un código QR desde la cámara en tiempo real.
#     """
#     # Inicializa la captura de video desde la cámara (cámara 0 por defecto)
#     cap = cv2.VideoCapture(0)
#     # Reducir la resolución del video para mejorar la velocidad de procesamiento
#     cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
#     cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

#     # Bucle infinito para capturar y procesar frames de la cámara en tiempo real
#     while True:
#         # Captura el frame actual de la cámara
#         # "_" es una variable de descarte para el estado de éxito de la captura, que no usamos
#         _, frame = cap.read()

#         # Convertir el frame a escala de grises para facilitar la detección
#         gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

#         # Aplicar desenfoque para reducir el ruido en la imagen
#         blurred = cv2.GaussianBlur(gray, (5, 5), 0)

#         # Intentar decodificar los códigos QR desde la imagen preprocesada
#         qrs = decode(blurred)

#         # Si se detecta algún QR, este bucle for lo procesará
#         for qr in qrs:
#             # Decodifica los datos del QR de formato bytes a string
#             qr_data = qr.data.decode('utf-8')

#             # Muestra los datos del QR en la consola
#             print("QR Data:", qr_data)

#             # Devuelve los datos del QR y termina la función (sale del bucle)
#             return qr_data
        
#         # Muestra el frame actual en una ventana de OpenCV con el título 'Escaner de QR'
#         cv2.imshow('Escaner de QR', frame)
        
#         # Si el usuario presiona la tecla 'q', se sale del bucle
#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break

#     # Libera el objeto de captura de video cuando el bucle termina
#     cap.release()

#     # Cierra todas las ventanas de OpenCV abiertas
#     cv2.destroyAllWindows()

#     # Si no se detectó ningún QR, devuelve None
#     return qr_data

qr_data_global = None
def read_qr_camera():
    """
    Lee un código QR desde la cámara en tiempo real.
    """
    qr_data = None
    # Inicializa la captura de video desde la cámara (cámara 0 por defecto)
    cap = cv2.VideoCapture(0)
    # Reducir la resolución del video para mejorar la velocidad de procesamiento
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    # Bucle infinito para capturar y procesar frames de la cámara en tiempo real
    while True:
        # Captura el frame actual de la cámara
        # "_" es una variable de descarte para el estado de éxito de la captura, que no usamos
        _, frame = cap.read()

        # Convertir el frame a escala de grises para facilitar la detección
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Aplicar desenfoque para reducir el ruido en la imagen
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)

        # Intentar decodificar los códigos QR desde la imagen preprocesada
        qrs = decode(blurred)

        # Si se detecta algún QR, este bucle for lo procesará
        for qr in qrs:
            # Decodifica los datos del QR de formato bytes a string
            qr_data = qr.data.decode('utf-8')

            # Muestra los datos del QR en la consola
            print("QR Data:", qr_data)

            # Si el usuario presiona la tecla 'q', se sale del bucle
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            # Cierra todas las ventanas de OpenCV abiertas
            cv2.destroyAllWindows()


            # Devuelve los datos del QR y termina la función (sale del bucle)
            return qr_data
        
        # Muestra el frame actual en una ventana de OpenCV con el título 'Escaner de QR'
        cv2.imshow('Escaner de QR', frame)
        
        # Si el usuario presiona la tecla 'q', se sale del bucle
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Libera el objeto de captura de video cuando el bucle termina
    cap.release()

    # Cierra todas las ventanas de OpenCV abiertas
    cv2.destroyAllWindows()

    # Si no se detectó ningún QR, devuelve None
    return qr_data


