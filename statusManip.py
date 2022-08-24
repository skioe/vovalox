from textAdd import database, add_new_person, change_status
from vk_api.utils import get_random_id


def check_and_edit(vk, target_person, chat_id, status):
    if target_person not in database.keys():
        add_new_person(target_person)
        send_message(vk,
                     chat_id,
                     f"@id{target_person} (Юзер) успешно добавлен в базу!",
                     None)
    if database[target_person]["status"] != status:
        change_status(target_person, status)
        send_message(vk,
                     chat_id,
                     f"Теперь @id{target_person} (Юзер) - {status}!",
                     None)


def send_message(vk, chat_id, message, attachments):
    vk.messages.send(
        random_id=get_random_id(),
        attachment=attachments,
        chat_id=chat_id,
        message=message
    )
