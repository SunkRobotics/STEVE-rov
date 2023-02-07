import cv2
import base64

cap = cv2.VideoCapture(0)

while True:
    _, frame = cap.read()
    byte_img = cv2.imencode('.jpg', frame)[1]
    print(base64.b64encode(byte_img))