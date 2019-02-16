import asyncio
import json


def load_image(filename):
    with open(filename, "rb") as file:
        data = file.read()
    return data


async def client(message):
    reader, writer = await asyncio.open_connection("127.0.0.1", 8888)

    writer.write(message)

    if writer.can_write_eof():
        writer.write_eof()

    print("Image sended")

    data = (await reader.read()).decode()

    people = json.loads(data)[0].get('people', 'corrupted JSON')

    print(f"Who is in the image:", *people)

    print("Close the connection")
    writer.close()


if __name__ == "__main__":
    while True:
        filename = input("Type the relative path of some image: ")
        
        if filename == 'exit':
            break
        
        image_content = load_image(filename)
        asyncio.run(client(image_content))
