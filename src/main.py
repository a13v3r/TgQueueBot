import telebot

from bot_instructions import *
from BotCommands import TgBot
from src.bot_helper import bot_token

bot = telebot.TeleBot(bot_token)


@bot.message_handler(commands=[START])
def start_message(message):
    bot.send_message(message.chat.id, COMMANDS_DESCRIPTION[START])


@bot.message_handler(commands=[HELP])
def help_message(message):
    bot.send_message(message.chat.id, HELP_DESCRIPTION)


@bot.message_handler(commands=[CREATE_GROUP])
def create_group_message(message):
    command = TgBot(bot, message)
    command.create_group()


@bot.message_handler(commands=[DELETE_GROUP])
def delete_group_message(message):
    command = TgBot(bot, message)
    command.delete_group()


@bot.message_handler(commands=[GET_GROUP])
def get_group_message(message):
    command = TgBot(bot, message)
    command.get_group()


@bot.message_handler(commands=[GET_ALL_GROUPS])
def get_all_groups_message(message):
    command = TgBot(bot, message)
    command.get_all_groups()


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.inline_message_id:
        command = TgBot(bot, call)
        if call.data[:len(answer := CALLBACK_INLINE_SPIN)] == answer:
            command.do_inline_spin()
        elif call.data[:len(answer := CALLBACK_INLINE_QUEUE_NEXT)] == answer:
            command.inline_next_pos_in_queue()
        elif call.data[:len(answer := CALLBACK_INLINE_QUEUE_PREVIOUS)] == answer:
            command.inline_prev_pos_in_queue()
        elif call.data[:len(answer := CALLBACK_INLINE_QUEUE_DELETE)] == answer:
            command.inline_delete_queue()
        elif call.data[:len(answer := CALLBACK_INLINE_QUEUE_SKIP)] == answer:
            command.skip_pos_queue()
        elif call.data[:len(answer := CALLBACK_INLINE_GROUP_SHUFFLE)] == answer:
            command.do_inline_create_queue(1)
        elif call.data[:len(answer := CALLBACK_INLINE_GROUP_NORMAL)] == answer:
            command.do_inline_create_queue(0)


@bot.inline_handler(lambda query: len(query.query) == 0)
def default_query(query):
    command = TgBot(bot, query)
    command.inline_handler_empty()


@bot.inline_handler(lambda query: len(query.query) > 0)
def query_text(query):
    command = TgBot(bot, query)
    command.inline_handler_not_empty()


if __name__ == '__main__':
    bot.infinity_polling()
