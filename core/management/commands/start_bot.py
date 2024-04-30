import telebot
from django.core.management import BaseCommand
from telebot import types
import time
from math import sqrt
from django.conf import settings

from core.bot_handler import BotHandler

bot = telebot.TeleBot(settings.TG_BOT)
bot_handler = BotHandler(bot)

@bot.message_handler(commands=['start'])
def start(message):
    print(message.chat.id)
    try:
        bot_handler.handle_start(message)
    except Exception as exception:
        print("Exception occured: " + str(exception))

@bot.message_handler(content_types=['text'])
def after_text(message):
    bot_handler.handle_text(message)
...


def after_text_2(message):
   print('введённый пользователем номер телефона на шаге "смс":', message.text)

@bot.callback_query_handler(func=lambda callback: True)
def main(callback):
    print("callback")
    print(str(callback.__dict__))
    try:
        bot_handler.handle_main(callback)
    except Exception as exception:
        print("Exception occured: " + str(exception))

class Command(BaseCommand):

    def handle(self, *args, **options):
        while True:
            try:
                bot.polling(none_stop=True)
            except Exception as ex:
                print(ex)
                time.sleep(10)