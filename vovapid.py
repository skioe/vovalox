import vk_api
import random

from vk_api.utils import get_random_id
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType

vk_session = vk_api.VkApi(token = os.getenv('tokenHeroku'))
longpoll = VkBotLongPoll(vk_session, 193102999)
vk = vk_session.get_api()

def main():

    for event in longpoll.listen():

        if event.type == VkBotEventType.MESSAGE_NEW and event.from_chat:

            print(f"{event.message.text}\n{event.chat_id}\n{event.message['from_id']}\n")

            msgRec = event.message.text.lower()

            if event.message['from_id'] == 152663635:
                
                vk.messages.send(
                    random_id = get_random_id(),
                    attachment = ("photo-183016631_457239293", "audio491457183_456242598"),
                    chat_id = event.chat_id,
                    )

            if event.message['from_id'] == 121418529:
   
                vk.messages.send(
                    random_id = get_random_id(),
                    attachment = ("photo-183016631_457239294", "audio121418529_456240234"),
                    chat_id = event.chat_id,
                    )

if __name__ == "__main__":
    main()
