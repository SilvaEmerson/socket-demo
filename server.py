import asyncio
import os
from random import randint

from image_clf import predict


def save_image(filename, data):
    with open(filename, "wb") as file:
        file.write(data)


async def handler(reader, writer):
    image = await reader.read()
    filename = f"./{randint(0, 10)}.jpeg"
    
    save_image(filename, image)
    prediction = predict(filename)

    print(prediction)
    os.remove(filename)
    
    writer.write(prediction.encode())
    await writer.drain()

    print("Close the connection")
    writer.close()


async def main():
    server = await asyncio.start_server(handler, "127.0.0.1", 8888)

    addr = server.sockets[0].getsockname()
    print(f"Serving on {addr}")

    async with server:
        await server.serve_forever()


asyncio.run(main())
