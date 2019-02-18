import asyncio
import os
import json
from random import randint

import numpy as np
import matplotlib.pyplot as plt

from image_clf import predict, KNOWN_PEOPLE_DIR


def save_image(filename, data):
    data = np.array(data, dtype=np.uint8)
    plt.imsave(filename, data)


def setup(method=None, name=None, **kwargs):
    return {
        "ADD": (os.path.join(KNOWN_PEOPLE_DIR, name), on_add),
        "PREDICT": (name, on_predict),
    }[method]


def on_add(filename):
    return json.dumps([{"answer": "Saved %s" % filename}])


def on_predict(filename):
    prediction = predict(filename)
    os.remove(filename)
    return prediction


async def handler(reader, writer):
    message = json.loads((await reader.read()).decode())
    filename, action = setup(**message)

    save_image(filename, message.get("content"))
    response = action(filename)

    print(response)

    writer.write(response.encode())
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
