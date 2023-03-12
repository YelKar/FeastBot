import os

import response
from fetes import Feasts
from telebot import TeleBot
from telebot.types import Message

from util import reference

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


bot.infinity_polling()
