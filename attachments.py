from textAdd import database
from textAdd import make_image
import random


def build_attachments(from_id, photo):
    attachments = []

    attachments.append(database[from_id]['audio'])
    attachments.append(f"photo{photo['owner_id']}_{photo['id']}")

    return attachments


def upload_photo(from_id, msg_rec):
    images_list = database[from_id].get("images", [])
    image = random.choice(images_list)
    out_image = f"temp_{image}"
    make_image(msg_rec, image, out_image)
    return f"temp_images/{out_image}"
