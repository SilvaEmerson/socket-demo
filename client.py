import asyncio
import json

import matplotlib.pyplot as plt


def load_image(filename):
    return plt.imread(filename).tolist()


def unknow_people_num(people):
    return people.count("Unknow person")


def gen_message(method, filename, content):
    return json.dumps({"method": method, "name": filename, "content": content}).encode()


def on_predict(data):
    people = data[0].get("answer", "corrupted JSON")
    unknow_people = unknow_people_num(people)
    known_people = filter(lambda person: person != "Unknow person", people)
    
    print(f"Who is in the image:")
    
    if not unknow_people:
       print(*known_people, sep=" and ")
    else:
       print(*known_people, "%d unknow people/person" % unknow_people, sep=" and ") 


async def client(message):
    actions = {"ADD": lambda data: print(data[0]["answer"]), "PREDICT": on_predict}

    reader, writer = await asyncio.open_connection("127.0.0.1", 8888)

    writer.write(message)

    if writer.can_write_eof():
        writer.write_eof()

    print("Image sended")

    data = (await reader.read()).decode()

    requested_method = json.loads(message.decode())["method"]
    actions[requested_method](json.loads(data))

    print("Close the connection")
    writer.close()


if __name__ == "__main__":
    while True:
        method = input("Type the method (ADD or PREDICT)\ntype 'exit' to quit: ")

        if method == "exit":
            break

        filename = input("Type the relative path of some image: ")
        image_content = load_image(filename)
        asyncio.run(client(gen_message(method, filename, image_content)))
