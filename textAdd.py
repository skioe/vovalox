import fnmatch
import os
import textwrap
from json import load, dump
from shutil import copyfile

from PIL import Image, ImageFont
from pilmoji import Pilmoji

with open('persons.json') as load_database:
    database = load(load_database)


def dump_db():
    with open("persons.json", "w") as write_database:
        dump(database, write_database, indent=4)


def change_status(target_person, status):
    database[target_person]["status"] = status
    if status == "chad":
        database[target_person]["audio"] = "audio121418529_456240234"
    if status == "virgin":
        database[target_person]["audio"] = "audio491457183_456242598"

    dump_db()

    copyfile(f"images/{status}.jpg", f"images/{target_person}.jpg")


def add_new_person(user_id):
    database[user_id] = {
        "name": user_id,
        "audio": "",
        "images": [f"{user_id}.jpg"],
        "status": ""
    }

    dump_db()


def process_new_images():
    for user_id in database:
        name = database[user_id]["name"]
        images_list = [img for img in os.listdir("images") if
                       img.startswith(name) and (img.endswith(".jpg") or img.endswith(".png"))]
        database[user_id]["images"] = images_list

    dump_db()


def make_image(text, in_image, out_image):
    image = Image.open("images/" + in_image)
    font = ImageFont.truetype("fonts/Ubuntu-B.ttf", 37)

    margin = offset = 20
    with Pilmoji(image) as pilmoji:
        for line in textwrap.wrap(text, width=32):
            pilmoji.text((margin, offset), line, font=font, fill='black')
            offset += font.getsize(line)[1]
    image.save("temp_images/" + out_image)
