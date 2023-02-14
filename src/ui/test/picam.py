from picamera2 import Picamera2
from picamera2.outputs import FileOutput
from picamera2.encoders import JpegEncoder
import io
import asyncio
from websockets import serve


class WSServer:
    buffer = io.BytesIO()

    @classmethod
    async def send_bytes(cls, websocket, path):

        while True:
            print(bytes(cls.buffer))
            await websocket.send(cls.buffer)
            await asyncio.sleep(0.5)

    @classmethod
    async def picamera_server(cls):
        picam2 = Picamera2()
        #  picam2.set_controls({"AfMode": 2})
        picam2.configure(picam2.create_video_configuration(
            main={"size": (1280, 720)}))
        picam2.start_recording(JpegEncoder(), FileOutput(cls.buffer))

        while True:
            print("ooga")
            await asyncio.sleep(0.5)


def main():
    loop = asyncio.get_event_loop()
    ws_server = serve(
        WSServer.send_bytes, "0.0.0.0", 3000, ping_interval=None
    )
    asyncio.ensure_future(WSServer.picamera_server())
    asyncio.ensure_future(ws_server)
    loop.run_forever()


if __name__ == "__main__":
    main()
