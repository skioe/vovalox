import vk_api
import os

from vk_api import VkUpload
from vk_api.utils import get_random_id
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType

from textAdd import database, process_new_images
from config import TOKEN, GROUP_ID
from statusManip import command_sender_check
from attachments import build_attachments, upload_photo

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
            chat_id = event.chat_id

            first_word = msg_rec.split(" ")[0]

            if from_id in database.keys() and first_word != "!chad" and first_word != "!virgin":
                attachments = build_attachments(from_id, upload.photo_messages(upload_photo(from_id, msg_rec))[0])
                send_message(
                    chat_id,
                    None,
                    attachments=attachments
                )

            if first_word == "!chad" or first_word == "!virgin":
                status = first_word[1:]
                send_message(
                    chat_id=chat_id,
                    message=command_sender_check(msg_rec, from_id, status),
                    attachments=None
                )

            if first_word == "!status":
                send_message(
                    chat_id=chat_id,
                    message=command_sender_check(msg_rec, status_check=True),
                    attachments=None
                )


def send_message(chat_id, message, attachments):
    vk.messages.send(
        random_id=get_random_id(),
        chat_id=chat_id,
        attachment=attachments,
        message=message
    )


if __name__ == "__main__":
    main()
