import telebot
import time
from telebot import types
from celery import shared_task
from django.conf import settings

from core.bot_handler import introduction_text2
from core.models import Tester, Mark, AudioFiles, ErrorLog

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
        time.sleep(6)

@shared_task
def retry_error(tester_id, error_log_id):
    time.sleep(11)
    tester = Tester.objects.get(pk=int(tester_id))
    error_log = ErrorLog.objects.get(pk=int(error_log_id))
    from core.bot_handler import BotHandler
    if error_log.type == "_send_next_file":
        bot = telebot.TeleBot(settings.TG_BOT)
        handler = BotHandler(bot=bot, retry=True)
        if handler._send_next_file(tester.chat_id, tester):
            error_log.success_resend = True
            error_log.save()


@shared_task
def test_tasks():
    import time
    print("test_tasks")
    bot = telebot.TeleBot(settings.TG_BOT)
    a = bot.send_message("265757675", "Hello1")
    print(a.__dict__)
