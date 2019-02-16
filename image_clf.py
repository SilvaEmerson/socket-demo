import face_recognition as fr
import json
import os


def predict_mock(file):
    return json.dumps({"result": "diasbdiasbdaibd"})


def predict(file):
    img = fr.load_image_file(file)
    img = fr.face_encodings(img)
    KNOWN_PERSONS = "./images"

    know_images = [
        *map(lambda file: os.path.join(KNOWN_PERSONS, file), os.listdir(KNOWN_PERSONS))
    ]

    know_images_encoded = [
        fr.face_encodings(fr.load_image_file(img))[0] for img in know_images
    ]

    if len(img) == 0:
        return json.dumps(
            [{"response": "An error hapenned, please choose another picture"}]
        )
    elif len(img) > 1:
        know_images_names = [i.rsplit(".", 1)[0] for i in know_images]
        results = []
        for i in img:
            matches = fr.compare_faces(know_images_encoded, i)
            name = "Unknow person"

            if True in matches:
                first_match_index = matches.index(True)
                name = know_images_names[first_match_index]

            results.append(name)

        return json.dumps([{"response": results}])

    img = img[0]

    results = fr.compare_faces(know_images_encoded, img)

    if results.count(False) == len(results):
        return json.dumps([{"response": "Unknow person"}])

    result = {
        i[0]: i[1]
        for i in zip(results, os.listdir(KNOWN_PERSONS))
    }

    return json.dumps([{"response": result[True].rsplit(".", 1)[0]}])
