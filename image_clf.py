import face_recognition as fr
import json
import os


def predict(file):
    img = fr.load_image_file(file)
    img = fr.face_encodings(img)
    KNOWN_PERSONS = "./images"

    known_images = [
        os.path.join(KNOWN_PERSONS, file) for file in os.listdir(KNOWN_PERSONS)
    ]

    known_images_encoded = [
        fr.face_encodings(fr.load_image_file(img))[0] for img in known_images
    ]

    if len(img) == 0:
        return json.dumps(
            [{"people": "An error hapenned, please choose another picture"}]
        )
    elif len(img) > 1:
        known_images_names = [i.rsplit(".", 1)[0] for i in known_images]
        results = []
        for i in img:
            matches = fr.compare_faces(known_images_encoded, i)
            name = "Unknow person"

            if True in matches:
                first_match_index = matches.index(True)
                name = known_images_names[first_match_index]

            results.append(name)

        return json.dumps([{"people": results}])

    img = img[0]

    results = fr.compare_faces(known_images_encoded, img)

    if results.count(False) == len(results):
        return json.dumps([{"people": "Unknow person"}])

    answer = {
        i[0]: i[1]
        for i in zip(results, os.listdir(KNOWN_PERSONS))
    }

    return json.dumps([{"people": answer[True].rsplit(".", 1)[0]}])
