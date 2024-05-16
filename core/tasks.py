import telebot
from telebot import types
from celery import shared_task
from django.conf import settings
from core.models import Day, Tester
from core.utils import get_today

@shared_task
def start_new_day():
    # Task logic here
    block = 1
    days = Day.objects.all().order_by("-id")
    if len(days) != 0:
        block = days[0].block+1
    day = Day()
    day.day = get_today()
    day.block = block
    day.save()

    bot = telebot.TeleBot(settings.TG_BOT)

    testers = Tester.objects.all()
    for tester in testers:
        markup = types.InlineKeyboardMarkup()
        begin_button = types.InlineKeyboardButton('Начать', callback_data='begin')
        markup.row(begin_button)
        bot.send_message(tester.chat_id,
                         f'Сегодня '+str(block)+' день оценки. Для вас подготовлено 30 исполнителей', reply_markup=markup)

@shared_task
def test_tasks():
    print("test_tasks")