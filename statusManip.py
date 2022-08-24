from textAdd import database, add_new_person, change_status
import re


def correct_user_check(msg_rec):
    try:
        int(msg_rec.split(' ')[1])
        return True
    except ValueError:
        return False


def find_target_person(msg_rec):
    return " ".join(re.findall(r"\[id(\d*)\|.*]", msg_rec.split(' ')[1]))


def check_and_edit(target_person, status):

    if target_person not in database.keys():
        add_new_person(target_person)
        change_status(target_person, status)

        return f"@id{target_person} (Юзер) успешно добавлен в базу!"

    if database[target_person]["status"] != status:
        change_status(target_person, status)

        return f"Теперь @id{target_person} (Юзер) - {status}!"


def command_sender_check(msg_rec, from_id=None, status=None, status_check=None):

    if not correct_user_check(msg_rec):

        return "Юзер указан неверно!"

    target_person = find_target_person(msg_rec)
    if target_person in database.keys() and status_check:
        return f"@id{target_person} (Юзер) - {database[target_person]['status']}"
    if target_person not in database.keys() and status_check:
        return f"@id{target_person} (Юзера) нет в базе"

    if from_id != "121418529":

        return "А еще че?"

    return check_and_edit(target_person, status)


