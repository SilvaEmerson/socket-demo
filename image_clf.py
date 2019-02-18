import face_recognition as fr
import json
import os
import re


KNOWN_PEOPLE_DIR = "./images"


def get_person_name(filename):
    matchs = re.findall("(.+)\.", filename)
    return matchs[0]


def predict(file):
    img = fr.load_image_file(file)
    current_img = fr.face_encodings(img)

    # get full path of known people images
    known_images = [
        os.path.join(KNOWN_PEOPLE_DIR, file) for file in os.listdir(KNOWN_PEOPLE_DIR)
    ]

    # get encodings of all known people images
    known_images_encoded = [
        fr.face_encodings(fr.load_image_file(img))[0] for img in known_images
    ]

    # if current image has no one face
    if len(current_img) == 0:
        return json.dumps(
            [{"answer": "An error hapenned, please choose another picture"}]
        )
    # if current image has more than one faces
    elif len(current_img) > 1:
        known_images_names = [
            get_person_name(image) for image in os.listdir(KNOWN_PEOPLE_DIR)
        ]
        results = []
        for face in current_img:
            matches = fr.compare_faces(known_images_encoded, face)
            name = "Unknow person"

            if True in matches:
                first_match_index = matches.index(True)
                name = known_images_names[first_match_index]

            results.append(name)

        return json.dumps([{"answer": results}])

    current_img = current_img[0]

    results = fr.compare_faces(known_images_encoded, current_img)

    if results.count(False) == len(results):
        return json.dumps([{"answer": "Unknow person"}])

    answer = {i[0]: i[1] for i in zip(results, os.listdir(KNOWN_PEOPLE_DIR))}

    return json.dumps([{"answer": [get_person_name(answer[True])]}])
