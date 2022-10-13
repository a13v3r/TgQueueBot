from bot_instructions import *
from telebot import types


class QueueKeyboard:
    def __init__(self, call_data):
        self.data = call_data

    def callback_button_prev(self):
        return types.InlineKeyboardButton(text="Previous",
                                          callback_data=(answer := CALLBACK_INLINE_QUEUE_PREVIOUS) +
                                                        f"{self.data[len(answer):]}"
                                          )

    def callback_button_next(self):
        return types.InlineKeyboardButton(text="Next",
                                          callback_data=(answer := CALLBACK_INLINE_QUEUE_NEXT) +
                                                        f"{self.data[len(answer):]}")

    def callback_button_skip(self):
        return types.InlineKeyboardButton(text="Skip Person",
                                          callback_data=(answer :=CALLBACK_INLINE_QUEUE_SKIP) +
                                                        f"{self.data[len(answer):]}")

    def callback_button_delete(self):
        return types.InlineKeyboardButton(text="Delete Queue",
                                          callback_data=(answer := CALLBACK_INLINE_QUEUE_DELETE) +
                                                        f"{self.data[len(answer):]}")
