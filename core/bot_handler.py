import telebot
from telebot import types

from core.models import AudioFiles, Tester, Mark, Day
from core.utils import get_today

from django.conf import settings

class BotHandler:
    def __init__(self, bot):
        self.bot = bot
        pass

    def handle_start(self, message):

        day, created = Day.objects.get_or_create(day=get_today())
        if created:
            max_day = Day.objects.all().order_by("-block")[0]
            new_block = max_day.block+1
            day.block = new_block
            day.save()

        tg_id = message.from_user.id
        first_name = message.from_user.first_name
        last_name = message.from_user.last_name
        username = message.from_user.username

        print("HELLO!")
        print(tg_id)
        print(first_name)
        print(last_name)
        print(username)

        testers = Tester.objects.filter(tg_id=tg_id)
        if len(testers)==0:
            tester = Tester(tg_id=tg_id, first_name=first_name, last_name=last_name, username=username)
            tester.save()
        else:
            tester = testers[0]

        markup = types.InlineKeyboardMarkup()
        begin_button = types.InlineKeyboardButton('Начать', callback_data='begin')
        markup.row(begin_button)

        self.bot.send_message(message.chat.id,
                              f'Привет, '+tester.first_name+',добро пожаловать в этот прекрасный бот',
                              reply_markup=markup)

    def handle_main(self, callback):
        if callback.data == 'begin':
            self._handle_begin(callback)
        elif callback.data.startswith("setvalue_"):
            self._handle_make(callback)


    def _handle_begin(self, callback):
        day, created = Day.objects.get_or_create(day=get_today())

        tg_id = callback.from_user.id
        testers = Tester.objects.filter(tg_id=tg_id)
        if len(testers) == 0:
            return

        tester = testers[0]
        self._send_next_file(callback=callback, tester=tester, day=day)

    def _handle_make(self, callback):
        ss = callback.data.split("_")
        audio_file_id = int(ss[1])
        value = int(ss[2])

        day, created = Day.objects.get_or_create(day=get_today())

        tg_id = callback.from_user.id
        testers = Tester.objects.filter(tg_id=tg_id)
        if len(testers) == 0:
            return

        tester = testers[0]

        if Mark.objects.filter(tester=tester, audio_id=audio_file_id).count() > 0:
            self.bot.send_message(callback.message.chat.id,
                                  f'Вы уже проголосовали за это аудио')
            return

        mark = Mark(tester=tester, audio_id=audio_file_id, value=value, day=day)
        mark.save()

        self.bot.send_message(callback.message.chat.id,
                              f'Ваша оценка принята')

        self._send_next_file(callback=callback, tester=tester, day=day)

    def _send_next_file(self, callback, tester, day):
        if Mark.objects.filter(tester=tester, day=day).count() >= AudioFiles.objects.filter(block=day.block).count():
            self.bot.send_message(callback.message.chat.id,
                                  f'Хватит на сегодня')
            return
        latest_mark = Mark.objects.filter(tester=tester).order_by('-id').first()
        if latest_mark is None:
            latest_mark_audio_id = 0
        else:
            latest_mark_audio_id=latest_mark.audio.id
        print("latest_mark_id: "+str(latest_mark_audio_id))
        next_audio = AudioFiles.objects.filter(id__gt=latest_mark_audio_id, active=True).order_by("id").first()

        if next_audio is None:
            self.bot.send_message(callback.message.chat.id,
                                  f'Аудио файлы закончились! Спасибо')
            return

        self.bot.send_message(callback.message.chat.id,
                              f'Ждите файл')

        self.bot.send_audio(chat_id=callback.message.chat.id, audio=open(next_audio.file.path, 'rb'))

        markup = types.InlineKeyboardMarkup()
        btn = types.InlineKeyboardButton("1", callback_data='setvalue_' + str(next_audio.id) + '_1')
        markup.row(btn)
        btn = types.InlineKeyboardButton("2", callback_data='setvalue_' + str(next_audio.id) + '_2')
        markup.row(btn)
        btn = types.InlineKeyboardButton("3", callback_data='setvalue_' + str(next_audio.id) + '_3')
        markup.row(btn)
        btn = types.InlineKeyboardButton("4", callback_data='setvalue_' + str(next_audio.id) + '_4')
        markup.row(btn)
        btn = types.InlineKeyboardButton("5", callback_data='setvalue_' + str(next_audio.id) + '_5')
        markup.row(btn)
        self.bot.send_message(callback.message.chat.id,
                              f'Пожалуйста, поставье оценку',
                              reply_markup=markup)