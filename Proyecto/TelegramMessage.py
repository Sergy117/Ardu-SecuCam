import cv2 as cv
import numpy as np
import requests
import time

# Configuración del bot de Telegram
BOT_TOKEN = '####'
CHAT_ID = '###'

# Función para enviar un mensaje y una imagen al bot de Telegram
def send_image_to_telegram(image_path, message):
    url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto'
    files = {'photo': open(image_path, 'rb')}
    data = {'chat_id': CHAT_ID, 'caption': message}
    requests.post(url, files=files, data=data)

# URLs de las cámaras
urlS = 'http://192.168.137.178'
urlL = 'http://192.168.137.250'
urlP = 'http://192.168.137.116'

streamS = f"{urlS}:81/stream"
streamL = f"{urlL}:81/stream"
streamP = f"{urlP}:81/stream"

# Función para reconectar a una cámara
def reconnect_camera(stream_url):
    return cv.VideoCapture(stream_url)

# Iniciar las cámaras
capS = reconnect_camera(streamS)
capL = reconnect_camera(streamL)
capP = reconnect_camera(streamP)

# Cargar el modelo detector de personas de OpenCV
hog = cv.HOGDescriptor()
hog.setSVMDetector(cv.HOGDescriptor_getDefaultPeopleDetector())

s = 0
l = 0
p = 0

while True:
    retS, frameS = capS.read()
    if not retS:
        print("Failed to grab S, reconnecting...")
        capS = reconnect_camera(streamS)
        continue

    # Detección de personas en la imagen de la cámara S
    detectedS, _ = hog.detectMultiScale(frameS)
    if len(detectedS) > 0:
        if s == 0:
            cv.imwrite('imgS.jpg', frameS)
            send_image_to_telegram('imgS.jpg', "Intruso en Camara S")
        s = len(detectedS)
    else:
        s = 0

    cv.imshow('EspcamS', frameS)

    retL, frameL = capL.read()
    if not retL:
        print("Failed to grab L, reconnecting...")
        capL = reconnect_camera(streamL)
        continue

    # Detección de personas en la imagen de la cámara L
    detectedL, _ = hog.detectMultiScale(frameL)
    if len(detectedL) > 0:
        if l == 0:
            cv.imwrite('imgL.jpg', frameL)
            send_image_to_telegram('imgL.jpg', "Intruso en Camara L")
        l = len(detectedL)
    else:
        l = 0

    cv.imshow('EspcamL', frameL)

    retP, frameP = capP.read()
    if not retP:
        print("Failed to grab P, reconnecting...")
        capP = reconnect_camera(streamP)
        continue

    # Detección de personas en la imagen de la cámara P
    detectedP, _ = hog.detectMultiScale(frameP)
    if len(detectedP) > 0:
        if p == 0:
            cv.imwrite('imgP.jpg', frameP)
            send_image_to_telegram('imgP.jpg', "Intruso en Camara P")
        p = len(detectedP)
    else:
        p = 0

    cv.imshow('EspcamP', frameP)

    if cv.waitKey(1) & 0xFF == ord('q'):
        break

capS.release()
capL.release()
capP.release()
cv.destroyAllWindows()
