import json
from src.bot_helper import path

path_to_groups = path+"/storage/groups.json"
path_to_users = path+"/storage/users.json"
path_to_msg = path+"/storage/messageState.json"

def set_new_group(user_id, group, group_name):
    arr = group.split('\n')
    group_list = []
    for el in arr:
        if not el.isspace() and not el == '':
            group_list.append(el)
    group_name = group_name.replace(" ", "")
    if group_name == "":
        return "Введите название группы!"
    # print(os.listdir())
    with open(path_to_groups, "r") as read_file:
        group_table = json.load(read_file)
    # print(group_table)
    if group_name in group_table:
        return "Группа с таким названием уже существует!"
    else:
        with open(path_to_users,
                  "r") as read_file:
            userdata = json.load(read_file)

        group_table[group_name] = group_list
        if user_id in userdata:
            userdata[user_id]['groups'].append(group_name)
        else:
            userdata[user_id] = {}
            userdata[user_id]['groups'] = [group_name]
            userdata[user_id]['level'] = 5
        if len(userdata[user_id]['groups']) > userdata[user_id]['level']:
            return "Внимание! Вы создали слишком много групп для вашего уровня доступа, обратитесь к администратору"
        with open(path_to_groups, "w") as data_file:
            json.dump(group_table, data_file)
        with open(path_to_users,
                  "w") as data_file:
            json.dump(userdata, data_file)

        if len(userdata[user_id]['groups']) == userdata[user_id]['level'] - 1:
            return "Внимание! Это последняя группа которую вы можете добавить для вашего уровня доступа"
        else:
            return f"Группа {group_name} добавлена успешно!"


def del_group(user_id, group_name):
    group_name = group_name.replace(" ", "")
    if group_name == "":
        return "Введите название группы!"
    # print(os.listdir())
    with open(path_to_groups, "r") as read_file:
        group_table = json.load(read_file)
    # print(group_table)
    if group_name not in group_table:
        return "Группы с таким названием и так не существует!"
    else:
        with open(path_to_users,
                  "r") as read_file:
            userdata = json.load(read_file)

        if user_id in userdata:
            if group_name in userdata[user_id]['groups']:
                userdata[user_id]['groups'].remove(group_name)
                with open(path_to_groups, "w") as data_file:
                    json.dump(group_table, data_file)
                with open(path_to_users,
                          "w") as data_file:
                    json.dump(userdata, data_file)

                return f"Группа {group_name} удалена успешно!"
            else:
                return "Это не ваша группа!"
        else:
            return "Вы не создали не одной группы!"


def set_start_queue_position(user_id, shuffled_group):
    with open(path_to_msg, "r") as read_file:
        msg_table = json.load(read_file)
    msg_table[user_id] = {}
    msg_table[user_id]['group'] = shuffled_group
    msg_table[user_id]['position'] = 0
    with open(path_to_msg, "w") as data_file:
        json.dump(msg_table, data_file)


def del_queue(message_id):
    with open(path_to_msg, "r") as read_file:
        msg_table = json.load(read_file)
    try:
        del msg_table[message_id]
        with open(path_to_msg, "w") as data_file:
            json.dump(msg_table, data_file)
        return "Очередь удалена!"
    except Exception as e:
        return e


def set_new_queue_position(message_id, step):
    with open(path_to_msg, "r") as read_file:
        msg_table = json.load(read_file)
    pos = msg_table[message_id]['position']
    pos += step
    msg_table[message_id]['position'] = pos
    with open(path_to_msg, "w") as data_file:
        json.dump(msg_table, data_file)
    return msg_table[message_id]


def set_new_group_order(user_id, arr):
    with open(path_to_msg, "r") as read_file:
        msg_table = json.load(read_file)
    msg_table[user_id]['group'] = arr
    with open(path_to_msg, "w") as data_file:
        json.dump(msg_table, data_file)


def get_group(group_name):
    group_name = group_name.replace(" ", "")
    if group_name == "":
        return "Введите название группы!"
    with open(path_to_groups, "r") as read_file:
        group_table = json.load(read_file)
    if group_name in group_table:
        return "\n".join(group_table[group_name])
    else:
        return "Такой группы не было создано!"


def get_all_groups():
    with open(path_to_groups, "r") as read_file:
        group_table = json.load(read_file)
    a = group_table.keys()
    return a
