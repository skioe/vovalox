import vk_api
import random
import os

from vk_api import VkUpload
from vk_api.utils import get_random_id
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType

from textAdd import make_image, database
from config import TOKEN, GROUP_ID

token = os.environ['ACCESS_TOKEN'] if os.environ['ACCESS_TOKEN'] else token = TOKEN
group_id = os.environ['GROUP_ID'] if os.environ['GROUP_ID'] else group_id = GROUP_ID

vk_session = vk_api.VkApi(token=token)
longpoll = VkBotLongPoll(vk_session, os.environ['GROUP_ID'])
upload = VkUpload(vk_session)
vk = vk_session.get_api()


def main():
    for event in longpoll.listen():

        if event.type == VkBotEventType.MESSAGE_NEW and event.from_chat:

            print(f"{event.message.text}\n{event.chat_id}\n{event.message['from_id']}\n")

            msg_rec = event.message.text.lower()
            from_id = str(event.message['from_id'])

            if from_id in database.keys():
                attachments = []

                audio = database[from_id].get("audio", None)
                images_lst = database[from_id].get("images", [])

                if audio:
                    attachments.append(audio)
                if images_lst:
                    image = random.choice(images_lst)
                    out_image = f"temp_{image}"
                    make_image(msg_rec, image, out_image)
                    photo = upload.photo_messages(photos=f"temp_images/{out_image}")[0]
                    attachments.append(
                        f"photo{photo['owner_id']}_{photo['id']}"
                    )

                vk.messages.send(
                    random_id=get_random_id(),
                    attachment=attachments,
                    chat_id=event.chat_id,
                )


if __name__ == "__main__":
    main()
