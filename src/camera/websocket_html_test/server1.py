import cv2
import asyncio
from websockets import serve


async def send(websocket):
    cap = cv2.VideoCapture(2)

    while cap.isOpened():
        _, frame = cap.read()
        byte_img = cv2.imencode('.jpg', frame)[1]

        await websocket.send(bytearray(byte_img))


async def echo(websocket):
    file = open("test.jpeg", "rb")
    data = file.read()
    print(type(data))
    await websocket.send(bytearray(data))
    file.close()


async def main():
    async with serve(send, "0.0.0.0", 4000):
        await asyncio.Future()  # run forever

asyncio.run(main())
