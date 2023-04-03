import asyncio
from websockets import serve

async def echo(websocket):
    file = open("test.jpeg", "rb")
    data = file.read()
    print(type(data))
    await websocket.send(bytearray(data))
    file.close()
        

async def main():
    async with serve(echo, "localhost", 4000):
        await asyncio.Future()  # run forever

asyncio.run(main())