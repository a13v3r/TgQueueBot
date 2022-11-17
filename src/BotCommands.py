import random
from time import sleep

from src.bot_helper import bot_tag
from bot_keyboards import *
from services import json_service


class TgBot:
    def __init__(self, bot, call_or_message):
        self.bot = bot
        self.callOrMessage = call_or_message

    def create_group(self):
        bot = self.bot
        message = self.callOrMessage
        if not message.reply_to_message:
            bot.send_message(message.chat.id, COMMANDS_DESCRIPTION[CREATE_GROUP])
        else:
            ans = json_service.set_new_group(str(message.from_user.id), message.reply_to_message.text,
                                             message.text[len(CREATE_GROUP) + 1:])
            bot.send_message(message.chat.id, ans)

    def delete_group(self):
        bot = self.bot
        message = self.callOrMessage
        ans = json_service.del_group(str(message.from_user.id), message.text[len(DELETE_GROUP) + 1:])
        bot.send_message(message.chat.id, ans)

    def get_group(self):
        bot = self.bot
        message = self.callOrMessage
        ans = json_service.get_group(message.text[len(GET_GROUP) + 1:])
        bot.send_message(message.chat.id, ans)

    def get_all_groups(self):
        bot = self.bot
        message = self.callOrMessage
        # ans = json_service.getAllGroups() TODO: Access levels
        bot.send_message(message.chat.id, "Access Denied!")

    def do_inline_spin(self):
        bot = self.bot
        call = self.callOrMessage
        s = call.data[len(CALLBACK_INLINE_SPIN):]
        for i in range(len(s) + 1):
            try:
                bot.edit_message_text(inline_message_id=call.inline_message_id, text=(s[i:] + ' ' + s[:i]))
            #   print(s[i::] + ' ' + s[:i])
            except Exception as e:
                print(e)
            sleep(.5)

    def do_inline_create_queue(self, need_to_shuffle):
        bot = self.bot
        call = self.callOrMessage
        if need_to_shuffle:
            group_name = call.data[len(CALLBACK_INLINE_GROUP_SHUFFLE):]
        else:
            group_name = call.data[len(CALLBACK_INLINE_GROUP_NORMAL):]
        group_name = group_name.replace(" ", "")
        arr = json_service.get_group(group_name).split('\n')
        if need_to_shuffle:
            if group_name == '':
                pass
            else:
                random.shuffle(arr)
        json_service.set_start_queue_position(call.inline_message_id, arr)
        ans = "\n".join(arr[:])
        ans += f'\n\n{1}/{len(arr)} Now:\n'
        ans += arr[0]
        keyboard = types.InlineKeyboardMarkup()
        buttons = QueueKeyboard(call.data)
        # keyboard.add(callback_button_prev)
        keyboard.add(buttons.callback_button_next())
        keyboard.add(buttons.callback_button_skip())
        bot.edit_message_text(inline_message_id=call.inline_message_id, text=ans, reply_markup=keyboard)

    def create_queue_from_msg(self, need_to_shuffle):
        bot = self.bot
        call = self.callOrMessage

        if need_to_shuffle:
            msg_id = call.data[len(CALLBACK_INLINE_QUEUE_SHUFFLE):]
        else:
            msg_id = call.data[len(CALLBACK_INLINE_QUEUE_NORMAL):]
        msg_id = msg_id.replace(" ", "")
        ans = json_service.get_queue(msg_id)
        print(ans)
        if '-1' in ans:
            self.priority_settings("Добавьте людей в очередь!\n Выбор приоритетов заново")
            return
        arr = ans['group']
        print(arr)
        if need_to_shuffle:
            arrs = {}
            for name in arr:
                id = name.find(" ")
                priority = name[:id]
                name = name[id+1:]
                if priority in arrs:
                    arrs[priority].append(name)
                else:
                    arrs[priority] = [name]

            arr = []
            print(arrs)
            for priority, group in arrs.items():
                random.shuffle(group)

                for name in group:
                    arr.append(f"{priority} {name}")

        json_service.set_start_queue_position(call.inline_message_id, arr)
        ans = "\n".join(arr[:])
        ans += f'\n\n{1}/{len(arr)} Now:\n'
        ans += arr[0]
        keyboard = types.InlineKeyboardMarkup()
        buttons = QueueKeyboard(call.data)
        # keyboard.add(callback_button_prev)
        keyboard.add(buttons.callback_button_next())
        keyboard.add(buttons.callback_button_skip())
        bot.edit_message_text(inline_message_id=call.inline_message_id, text=ans, reply_markup=keyboard)

    def add_to_queue_inline(self, priority, priority_levels):
        bot = self.bot
        call = self.callOrMessage
        from_user = str(priority) + " " + call.from_user.first_name + " " + call.from_user.last_name + " @" + call.from_user.username

        print(from_user)
        output = json_service.add_to_queu(from_user, call.inline_message_id)
        pos = output['position']
        arr = output['group']
        ans = "In queue:\n" + "\n".join(arr) + '\n'

        kb = types.InlineKeyboardMarkup()
        kb.add(
            types.InlineKeyboardButton(text="Start without shuffle",
                                       callback_data=f"{CALLBACK_INLINE_QUEUE_NORMAL}{call.inline_message_id}"
                                       ))
        kb.add(types.InlineKeyboardButton(text="Shuffle",
                                          callback_data=f"{CALLBACK_INLINE_QUEUE_SHUFFLE}{call.inline_message_id}"
                                          ))
        for i in range(1, priority_levels + 1):
            kb.add(types.InlineKeyboardButton(text=f"Priority {i}",
                                              callback_data=f"{CALLBACK_INLINE_QUEUE_ADD}_{i}_{priority_levels}"
                                              ))
        bot.edit_message_text(inline_message_id=call.inline_message_id, text=ans, reply_markup=kb)


    def queue_start(self, priority_levels):
        bot = self.bot
        call = self.callOrMessage
        results = []
        kb = types.InlineKeyboardMarkup()
        kb.add(
            types.InlineKeyboardButton(text="Start without shuffle", callback_data=f"{CALLBACK_INLINE_QUEUE_NORMAL}{call.inline_message_id}"
                                       ))
        kb.add(types.InlineKeyboardButton(text="Shuffle", callback_data=f"{CALLBACK_INLINE_QUEUE_SHUFFLE}{call.inline_message_id}"
                                          ))
        for i in range(1, priority_levels+1):
            kb.add(types.InlineKeyboardButton(text=f"Priority {i}",
                                              callback_data=f"{CALLBACK_INLINE_QUEUE_ADD}_{i}_{priority_levels}"
                                              ))

        bot.edit_message_text(inline_message_id=call.inline_message_id, text="Q:", reply_markup=kb)

    def priority_settings(self, msg = "Set priority levels amount:"):
        bot = self.bot
        call = self.callOrMessage
        kb = types.InlineKeyboardMarkup()
        for i in range(1,6):
            kb.add(types.InlineKeyboardButton(text=f"Priority levels: {i}",
                                              callback_data=f"{CALLBACK_INLINE_QUEUE_PRIORITY_START}{i}"
                                              ))

        bot.edit_message_text(inline_message_id=call.inline_message_id, text=msg, reply_markup=kb)


    def queue_setup(self):
        bot = self.bot
        query = self.callOrMessage
        try:
            results = []
            kb = types.InlineKeyboardMarkup()


            kb.add(types.InlineKeyboardButton(text="Edit priority",
                                              callback_data=f"{CALLBACK_INLINE_QUEUE_PRIORITY_SETTINGS}"
                                              ))

            single_msg = types.InlineQueryResultArticle(
                id="1", title="Queue",
                input_message_content=types.InputTextMessageContent(
                    message_text=f"Очередь \n Настройте количество приоритетов"), reply_markup=kb)
            results.append(single_msg)
            bot.answer_inline_query(query.id, results)
        except Exception as e:
            print(e)

    def inline_next_pos_in_queue(self):
        bot = self.bot
        call = self.callOrMessage
        output = json_service.set_new_queue_position(call.inline_message_id, 1)
        pos = output['position']
        arr = output['group']
        print(arr)
        keyboard = types.InlineKeyboardMarkup()
        buttons = QueueKeyboard(call.data)
        if pos >= len(arr):
            keyboard.add(buttons.callback_button_prev())
            keyboard.add(buttons.callback_button_delete())
            ans = "Последний в очереди:\n" + arr[0]
        elif pos + 1 == len(arr):
            keyboard.add(buttons.callback_button_prev())
            keyboard.add(buttons.callback_button_delete())
            ans = "Последний в очереди:\n" + arr[pos]
        else:
            ans = "\n".join(arr[pos:]) + '\n' + f'\n{pos + 1}/{len(arr)} Now:\n' + arr[pos]
            keyboard.add(buttons.callback_button_prev())
            keyboard.add(buttons.callback_button_skip())
            keyboard.add(buttons.callback_button_next())
        bot.edit_message_text(inline_message_id=call.inline_message_id, text=ans, reply_markup=keyboard)

    def inline_prev_pos_in_queue(self):
        bot = self.bot
        call = self.callOrMessage
        output = json_service.set_new_queue_position(call.inline_message_id, -1)
        pos = output['position']
        arr = output['group']

        keyboard = types.InlineKeyboardMarkup()
        buttons = QueueKeyboard(call.data)
        if pos<0:
            pos = 0
            ans = "\n".join(arr) + f'\n\n{pos + 1}/{len(arr)} Now:\n' + arr[pos]
            keyboard.add(buttons.callback_button_skip())
            keyboard.add(buttons.callback_button_next())
        elif pos == 0:
            keyboard.add(buttons.callback_button_next())
            keyboard.add(buttons.callback_button_skip())
            ans = "\n".join(arr[pos:]) + '\n\n' + "Первый в очереди:\n" + arr[pos]
        else:
            ans = "\n".join(arr[pos:]) + f'\n\n{pos + 1}/{len(arr)} Now:\n' + arr[pos]
            keyboard.add(buttons.callback_button_prev())
            keyboard.add(buttons.callback_button_skip())
            keyboard.add(buttons.callback_button_next())
        bot.edit_message_text(inline_message_id=call.inline_message_id, text=ans, reply_markup=keyboard)

    def inline_delete_queue(self):
        bot = self.bot
        call = self.callOrMessage
        ans = json_service.del_queue(call.inline_message_id)
        bot.edit_message_text(inline_message_id=call.inline_message_id, text=ans)

    def skip_pos_queue(self):
        bot = self.bot
        call = self.callOrMessage
        output = json_service.set_new_queue_position(call.inline_message_id, 0)
        pos = output['position']
        arr = output['group']
        print(pos)
        if len(arr) > 2:
            arr[pos] = arr[pos] + ' '
            arr.insert(pos + 2, arr[pos] + ' ')
            arr = arr[1:]
        elif len(arr) ==2:
            arr[1], arr[0] = arr[0],arr[1]
            pos = 0
        else:
            pos = 0

        json_service.set_new_group_order(call.inline_message_id, arr)

        keyboard = types.InlineKeyboardMarkup()
        buttons = QueueKeyboard(call.data)
        if pos + 1 == len(arr):
            keyboard.add(buttons.callback_button_prev())
            keyboard.add(buttons.callback_button_delete())
            ans = "Последний в очереди:\n" + arr[pos]
        elif pos == 0:
            keyboard.add(buttons.callback_button_skip())
            keyboard.add(buttons.callback_button_next())
            ans = "\n".join(arr[pos:]) + '\n\n' + "Первый в очереди:\n" + arr[pos]
        else:
            ans = "\n".join(arr[pos:]) + '\n' + f'\n{pos + 1}/{len(arr)} Now:\n' + arr[pos]
            keyboard.add(buttons.callback_button_prev())
            keyboard.add(buttons.callback_button_skip())
            keyboard.add(buttons.callback_button_next())
        bot.edit_message_text(inline_message_id=call.inline_message_id, text=ans, reply_markup=keyboard)

    def inline_handler_help(self):
        bot = self.bot
        query = self.callOrMessage
        try:
            results = []
            single_msg = types.InlineQueryResultArticle(
                id="1", title="Help",
                input_message_content=types.InputTextMessageContent(
                    message_text=f"Узнайте возможности бота в /help в лс бота {bot_tag}"))
            results.append(single_msg)
            bot.answer_inline_query(query.id, results)
        except Exception as e:
            print(e)

    def inline_handler_empty(self):
        self.queue_setup()

    def inline_handler_not_empty(self):
        bot = self.bot
        query = self.callOrMessage
        results = []
        if query.query in json_service.get_all_groups():
            kb = types.InlineKeyboardMarkup()
            kb.add(
                types.InlineKeyboardButton(text="Start without shuffle", callback_data=f"{CALLBACK_INLINE_GROUP_NORMAL}"
                                                                                       f"{query.query}"))
            kb.add(types.InlineKeyboardButton(text="Shuffle", callback_data=f"{CALLBACK_INLINE_GROUP_SHUFFLE}"
                                                                            f"{query.query}"))
            single_msg = types.InlineQueryResultArticle(
                id="1", title="Get Group",
                input_message_content=types.InputTextMessageContent(message_text=json_service.get_group(query.query)),
                reply_markup=kb
            )

            results.append(single_msg)

            bot.answer_inline_query(query.id, results)
        else:
            kb = types.InlineKeyboardMarkup()
            kb.add(types.InlineKeyboardButton(text="Spin", callback_data=f"{CALLBACK_INLINE_SPIN}{query.query}"))

            single_msg = types.InlineQueryResultArticle(
                id="2", title="Spin",
                input_message_content=types.InputTextMessageContent(message_text=query.query),
                reply_markup=kb
            )

            results.append(single_msg)
            bot.answer_inline_query(query.id, results)
