import cv2
from pyzbar.pyzbar import decode

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

def read_qr_camera():
    """
    Lee un código QR desde la cámara en tiempo real.
    """
    cap = cv2.VideoCapture(0)

    while True:
        _, frame = cap.read()
        qrs = decode(frame)

        for qr in qrs:
            qr_data = qr.data.decode('utf-8')
            print("QR Data:", qr_data)
            return qr_data
        
        # Mostrar el frame en tiempo real (opcional)
        cv2.imshow('Escaner de QR', frame)
        
        # Salir con la tecla 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    return None
