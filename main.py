import vk_api
import random
import os
import re

from vk_api import VkUpload
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType

from textAdd import make_image, database, process_new_images
from config import TOKEN, GROUP_ID
from statusManip import check_and_edit, send_message

try:
    token = os.environ['ACCESS_TOKEN']
    group_id = os.environ['GROUP_ID']
except KeyError:
    token = TOKEN
    group_id = GROUP_ID

vk_session = vk_api.VkApi(token=token)
longpoll = VkBotLongPoll(vk_session, group_id=group_id)
upload = VkUpload(vk_session)
vk = vk_session.get_api()


# OPTIONAL
# process_new_images()

def main():
    for event in longpoll.listen():

        if event.type == VkBotEventType.MESSAGE_NEW and event.from_chat:

            print(f"{event.message.text}\n{event.chat_id}\n{event.message['from_id']}\n")

            msg_rec = event.message.text.lower()
            from_id = str(event.message['from_id'])

            first_word = msg_rec.split(" ")[0]
            
            if from_id in database.keys() and first_word != "!chad" and first_word != "!virgin":
                attachments = []

                audio = database[from_id]['audio']
                images_list = database[from_id].get("images", [])

                if audio:
                    attachments.append(audio)
                if images_list:
                    image = random.choice(images_list)
                    out_image = f"temp_{image}"
                    make_image(msg_rec, image, out_image)
                    photo = upload.photo_messages(photos=f"temp_images/{out_image}")[0]
                    attachments.append(
                        f"photo{photo['owner_id']}_{photo['id']}"
                    )

                send_message(
                    vk,
                    event.chat_id,
                    None,
                    attachments
                )

            if first_word == "!chad" or first_word == "!virgin":
                if event.message['from_id'] != 121418529:
                    send_message(vk,
                                 event.chat_id,
                                 "А еще че?",
                                 None)
                if event.message['from_id'] == 121418529:
                    status = first_word[1:]
                    target_person = " ".join(re.findall(r"\[id(\d*)\|.*]", msg_rec.split(' ')[1]))
                    check_and_edit(vk, target_person, event.chat_id, status)

            if first_word == "!status":
                target_person = " ".join(re.findall(r"\[id(\d*)\|.*]", msg_rec.split(' ')[1]))
                if target_person in database.keys():
                    send_message(vk,
                                 event.chat_id,
                                 f"@id{target_person} (Юзер) - {database[target_person]['status']}!",
                                 None)
                if target_person not in database.keys():
                    send_message(vk,
                                 event.chat_id,
                                 f"@id{target_person} (Юзера) нет в базе",
                                 None)

if __name__ == "__main__":
    main()
