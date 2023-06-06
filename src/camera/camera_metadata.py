#!/usr/bin/python
from picamera2 import Picamera2
from picamera2.outputs import FileOutput
from picamera2.encoders import MJPEGEncoder
import io
import asyncio
from websockets import serve, ConnectionClosed


class StreamingOutput(io.BufferedIOBase):
    def __init__(self):
        self.metadata = None
        self.frame = None
        self.picam2 = None

    def write(self, buf):
        self.frame = buf
        if self.picam2:
            self.metadata = self.picam2.capture_metadata()


class WSServer:
    output = StreamingOutput()

    @classmethod
    async def handler(cls, websocket, path, output):
        print("Client connected!")
        try:
            while True:
                if cls.output.frame is None:
                    await asyncio.sleep(0.001)
                    continue

                await websocket.send(bytearray(cls.output.frame), bytearray(cls.output.metadata))
                await asyncio.sleep(0.001)

        except ConnectionClosed:
            print("Client disconnected!")


def main():
    picam2 = Picamera2()
    WSServer.output.picam2 = picam2
    picam2.set_controls({"AfMode": 2})
    picam2.configure(picam2.create_video_configuration(
        main={"size": (1920, 1080)}))
    picam2.start_recording(MJPEGEncoder(50_000_000),
                           FileOutput(WSServer.output))

    loop = asyncio.get_event_loop()
    ws_server = serve(
        WSServer.handler, "0.0.0.0", 3000, ping_interval=None
    )
    asyncio.ensure_future(ws_server)
    loop.run_forever()


if __name__ == "__main__":
    main()
