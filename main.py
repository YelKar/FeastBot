"""
TODO get today feasts
TODO get day feasts with description
"""


import os

import response
from feasts import Feasts
from telebot import TeleBot
from telebot.types import Message, CallbackQuery

from util import reference, KeyBoard

if __name__ == '__main__':
    from dotenv import load_dotenv
    load_dotenv(".env")

bot = TeleBot(os.getenv("TOKEN"), parse_mode="html")


@bot.message_handler(commands=["start"])
def start(message: Message):
    bot.send_message(message.chat.id, reference)


@bot.message_handler(commands=['today'])
def today(message: Message):
    feasts = Feasts()
    bot.send_message(
        message.chat.id,
        response.day(feasts.today())
    )


@bot.message_handler(commands=["tomorrow"])
def tomorrow(message: Message):
    feasts = Feasts()
    bot.send_message(
        message.chat.id,
        response.day(feasts[:1])
    )


@bot.message_handler(commands=["select"])
def select(message: Message):
    bot.send_message(message.chat.id, "Выберите месяц из перечня", reply_markup=KeyBoard.year())


@bot.message_handler(commands=['select_day'])
def get_month(message: Message, month=None):
    bot.send_message(message.chat.id, "Выберите день", reply_markup=KeyBoard.month(month))


@bot.callback_query_handler(func=lambda call: call.data.startswith("send_month"))
def send_month(callback: CallbackQuery):
    get_month(callback.message, int(callback.data.split("_")[-1]))


@bot.callback_query_handler(func=lambda call: call.data.startswith("send_day"))
def send_day(callback: CallbackQuery):
    *_, date = callback.data.split("_")
    day, month = date.split(".")
    feasts = Feasts()
    bot.send_message(callback.from_user.id, response.day(feasts[:int(day):int(month)]))


bot.infinity_polling()
