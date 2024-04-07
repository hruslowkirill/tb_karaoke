import telebot
from telebot import types

from core.models import AudioFiles, Tester


class BotHandler:
    def __init__(self, bot):
        self.bot = bot
        pass

    def handle_start(self, message):

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
        self.bot.send_message(callback.message.chat.id,
                              f'Ждите файл')
        audio_file = AudioFiles.objects.all().first()

        self.bot.send_audio(chat_id=callback.message.chat.id, audio=open(audio_file.file.path, 'rb'))

        markup = types.InlineKeyboardMarkup()
        btn = types.InlineKeyboardButton("1", callback_data='setvalue_1')
        markup.row(btn)
        btn = types.InlineKeyboardButton("2", callback_data='setvalue_2')
        markup.row(btn)
        btn = types.InlineKeyboardButton("3", callback_data='setvalue_3')
        markup.row(btn)
        btn = types.InlineKeyboardButton("4", callback_data='setvalue_4')
        markup.row(btn)
        btn = types.InlineKeyboardButton("5", callback_data='setvalue_5')
        markup.row(btn)
        self.bot.send_message(callback.message.chat.id,
                              f'Пожалуйста, поставье оценку',
                              reply_markup=markup)

    def _handle_make(self, callback):
        ss = callback.data.split("_")
        value = int(ss[1])

        self.bot.send_message(callback.message.chat.id,
                              f'Ваша оценка принята')

    def _send_next_file(self):
        pass
