from picamera2 import Picamera2
from picamera2.outputs import FileOutput
from picamera2.encoders import JpegEncoder
import io
import asyncio
import base64
from websockets import serve, ConnectionClosed


class StreamingOutput(io.BufferedIOBase):
    def __init__(self):
        self.frame = None

    def write(self, buf):
        self.frame = buf


class WSServer:
    output = StreamingOutput()

    @classmethod
    async def handler(cls, websocket, path):
        print("Client connected!")
        try:
            while True:
                if cls.output.frame is None:
                    continue
                str_data = base64.b64encode(cls.output.frame)

                await websocket.send(str_data)
                await asyncio.sleep(0.0001)

        except ConnectionClosed:
            print("Client disconnected!")


def main():
    picam2 = Picamera2()
    #  picam2.set_controls({"AfMode": 2})
    picam2.configure(picam2.create_video_configuration(
        main={"size": (1280, 720)}))
    picam2.start_recording(JpegEncoder(), FileOutput(WSServer.output))

    loop = asyncio.get_event_loop()
    ws_server = serve(
        WSServer.handler, "0.0.0.0", 3000, ping_interval=None
    )
    asyncio.ensure_future(ws_server)
    loop.run_forever()


if __name__ == "__main__":
    main()
