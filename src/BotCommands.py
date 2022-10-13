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

    def inline_next_pos_in_queue(self):
        bot = self.bot
        call = self.callOrMessage
        output = json_service.set_new_queue_position(call.inline_message_id, 1)
        pos = output['position']
        arr = output['group']

        keyboard = types.InlineKeyboardMarkup()
        buttons = QueueKeyboard(call.data)
        if pos + 1 == len(arr):
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
        if pos == 0:
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
        arr[pos], arr[pos + 1] = arr[pos + 1], arr[pos]

        json_service.set_new_group_order(call.inline_message_id, arr)

        keyboard = types.InlineKeyboardMarkup()
        buttons = QueueKeyboard(call.data)
        if pos + 1 == len(arr):
            keyboard.add(buttons.callback_button_prev())
            keyboard.add(buttons.callback_button_delete())
            ans = "Последний в очереди:\n" + arr[pos]
        else:
            ans = "\n".join(arr[pos:]) + '\n' + f'\n{pos + 1}/{len(arr)} Now:\n' + arr[pos]
            keyboard.add(buttons.callback_button_prev())
            keyboard.add(buttons.callback_button_skip())
            keyboard.add(buttons.callback_button_next())
        bot.edit_message_text(inline_message_id=call.inline_message_id, text=ans, reply_markup=keyboard)

    def inline_handler_empty(self):
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
