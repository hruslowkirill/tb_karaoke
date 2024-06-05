import telebot
from telebot import types
from celery import shared_task
from django.conf import settings

from core.bot_handler import introduction_text2
from core.models import Tester, Mark, AudioFiles

@shared_task
def start_new_day():
    # Task logic here

    bot = telebot.TeleBot(settings.TG_BOT)

    testers = Tester.objects.all()
    for tester in testers:
        if Mark.objects.filter(tester=tester, audio__block=tester.current_block).count() < AudioFiles.objects.filter(block=tester.current_block).count():
            continue
        if Mark.objects.filter(tester=tester).count() >= AudioFiles.objects.all().count():
            continue
        tester.current_block += 1
        tester.save()
        markup = types.InlineKeyboardMarkup()
        begin_button = types.InlineKeyboardButton('Начать', callback_data='begin')
        markup.row(begin_button)
        bot.send_message(tester.chat_id,
                         f'Сегодня '+str(tester.current_block)+' день оценки. Для вас подготовлено 30 исполнителей\n'+introduction_text2, parse_mode="Markdown", reply_markup=markup)

@shared_task
def test_tasks():
    import time
    print("test_tasks")
    bot = telebot.TeleBot(settings.TG_BOT)
    a = bot.send_message("265757675", "Hello1")
    print(a.__dict__)
