import asyncio
import numpy as np
from websockets import serve
import cv2
import base64


async def send(websocket):
    cap = cv2.VideoCapture(0)

    while cap.isOpened():
        _, frame = cap.read()
        byte_img = cv2.imencode('.jpg', frame)[1]
        str_data = base64.b64encode(byte_img)
        
        await websocket.send(str_data)

async def main():
    async with serve(send, "localhost", 3000):
        await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())
