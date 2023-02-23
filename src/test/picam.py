from picamera2 import Picamera2
from picamera2.outputs import FileOutput
from picamera2.encoders import JpegEncoder
import io
import asyncio
import base64
from websockets import serve


class WSServer:
    #  buffer = io.BytesIO()

    @classmethod
    async def send_bytes(cls, websocket, path):
        picam2 = Picamera2()
        #  picam2.set_controls({"AfMode": 2})
        picam2.configure(picam2.create_video_configuration(
            main={"size": (854, 480)}))
        picam2.start()
        #  picam2.start_recording(JpegEncoder(), FileOutput(cls.buffer))

        while True:
            buffer = io.BytesIO()
            picam2.capture_file(buffer, format='jpeg')
            str_data = base64.b64encode(buffer.getbuffer())
            await websocket.send(str_data)
            #  print(buffer.getbuffer().nbytes)
            await asyncio.sleep(0.01)

    @classmethod
    async def picamera_server(cls):
        picam2 = Picamera2()
        #  picam2.set_controls({"AfMode": 2})
        picam2.configure(picam2.create_video_configuration(
            main={"size": (854, 480)}))
        picam2.start()
        #  picam2.start_recording(JpegEncoder(), FileOutput(cls.buffer))

        while True:
            #  buffer = io.BytesIO()
            picam2.capture_file(cls.buffer, format='jpeg')
            print(cls.buffer.getbuffer().nbytes)
            await asyncio.sleep(0.5)


def main():
    loop = asyncio.get_event_loop()
    ws_server = serve(
        WSServer.send_bytes, "0.0.0.0", 3000, ping_interval=None
    )
    #  asyncio.ensure_future(WSServer.picamera_server())
    asyncio.ensure_future(ws_server)
    loop.run_forever()


if __name__ == "__main__":
    main()
