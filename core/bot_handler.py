import telebot
from telebot import types

from core.models import AudioFiles, Tester, Mark, ApplicationQuestion, ApplicationAnswer

from django.conf import settings

introduction_text = """
Здравствуйте! Мы благодарим вас за согласие участвовать в нашем исследовании. Наша компания исследует, как слушатели воспринимают пение не профессиональных исполнителей. 
\nЕжедневно в течение 10 дней вы будете получать по 30 записей песен, и вам нужно будет оценить их пение по пятибалльной шкале. Всего будет 300 треков.
\n
Заполните, пожалуйста, анкету
"""
introduction_text2 = """
При оценке исполнителей придерживайтесь следующей системы:
    • 5 — *Отлично*. Вам ОЧЕНЬ понравилось;
    • 4 — *Хорошо*. Вам понравилось, исполнитель хорошо поет;
    • 3 — *Удовлетворительно*. Исполнитель поет средне;
    • 2 — *Плохо*. Вам не понравилось, исполнитель поет плохо;
    • 1 — *Очень Плохо*. Исполнение крайне не понравилось.\n
*Внимание*! Исполнители — это обычные люди, не связанные с профессиональным пением. Представьте, что это поют ваши знакомые, друзья, люди, которые вас окружают.\n
*Важно*: не сравнивайте исполнения между собой. Исполнители выбраны случайным образом, оценки могут быть как все разные, так и все одинаковые. Полагайтесь только на свои ощущения.
"""

def send_new_day_message(bot, chat_id, block):
    bot.send_message(chat_id, f'Сегодня ' + str(block) + ' день оценки. Для вас подготовлено 30 исполнителей\n' + introduction_text2, parse_mode="Markdown")

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
            tester = Tester(tg_id=tg_id, first_name=first_name, last_name=last_name, username=username, chat_id=message.chat.id)
            tester.save()
        else:
            tester = testers[0]

        markup = types.InlineKeyboardMarkup()
        begin_button = types.InlineKeyboardButton('Начать', callback_data='begin')
        markup.row(begin_button)

        self.bot.send_message(message.chat.id,
                              introduction_text,
                              reply_markup=markup, parse_mode="Markdown")

    def handle_text(self, message):
        tg_id = message.from_user.id
        testers = Tester.objects.filter(tg_id=tg_id)
        tester = testers[0]
        if tester.name is None:
            tester.name = message.text
            tester.save()
            self._go_to_application(chat_id=message.chat.id, tester=tester)

    def handle_main(self, callback):
        if callback.data == 'begin':
            self._handle_begin(callback)
        elif callback.data.startswith("setvalue_"):
            self._handle_make(callback)
        elif callback.data.startswith("subanswer_"):
            self._handle_sub_answer(callback)


    def _handle_begin(self, callback):

        tg_id = callback.from_user.id
        testers = Tester.objects.filter(tg_id=tg_id)
        if len(testers) == 0:
            return

        tester = testers[0]

        if tester.last_question < ApplicationQuestion.objects.all().count():
            self.bot.send_message(callback.message.chat.id, "Заполните пожалуйста анкету")
            self._go_to_application(chat_id=callback.message.chat.id, tester=tester)
        else:
            self._send_next_file(callback=callback, tester=tester)

    def _handle_sub_answer(self, callback):
        ss = callback.data.split("_")
        question_id = int(ss[1])
        answer_id = int(ss[2])

        tg_id = callback.from_user.id
        testers = Tester.objects.filter(tg_id=tg_id).prefetch_related("answers")
        if len(testers) == 0:
            return
        tester = testers[0]

        if len(tester.answers.filter(application_questions__id=question_id))>0:
            self.bot.send_message(callback.message.chat.id, "Вы уже ответили на этот вопрос")
            return

        #for an in tester.answers.all():
        #    if an.application_questions.id == question_id:
        #        self.bot.send_message(callback.message.chat.id, "Вы уже ответили на этот вопрос")
        #        return

        tester.answers.add(ApplicationAnswer.objects.get(id=answer_id))
        tester.last_question = ApplicationQuestion.objects.get(id=question_id).n
        tester.save()

        if tester.last_question < ApplicationQuestion.objects.all().count():
            self._go_to_application(chat_id=callback.message.chat.id, tester=tester)
        else:
            send_new_day_message(self.bot, tester.chat_id, tester.current_block)
            self._send_next_file(callback=callback, tester=tester)

    def _go_to_application(self, chat_id, tester):
        if tester.name is None:
            self.bot.send_message(chat_id,
                                  "Ваше имя")
            return
        next_question = ApplicationQuestion.objects.get(n=tester.last_question+1)

        markup = types.InlineKeyboardMarkup()
        answers = ApplicationAnswer.objects.filter(application_questions=next_question).order_by("id")
        for a in answers:
            btn = types.InlineKeyboardButton(a.text, callback_data='subanswer_' + str(next_question.id)+"_"+str(a.id))
            markup.row(btn)

        self.bot.send_message(chat_id,
                              next_question.text, reply_markup=markup)

    def _handle_make(self, callback):
        print("_handle_make")
        ss = callback.data.split("_")
        audio_file_id = int(ss[1])
        value = int(ss[2])


        tg_id = callback.from_user.id
        testers = Tester.objects.filter(tg_id=tg_id)
        if len(testers) == 0:
            return

        tester = testers[0]

        if Mark.objects.filter(tester=tester, audio_id=audio_file_id).count() > 0:
            self.bot.send_message(callback.message.chat.id,
                                  f'Вы уже проголосовали за это аудио')
            return

        mark = Mark(tester=tester, audio_id=audio_file_id, value=value)
        mark.save()

        self.bot.send_message(callback.message.chat.id,
                              f'Ваша оценка принята')

        self._send_next_file(callback=callback, tester=tester)

    def _send_next_file(self, callback, tester):
        print("_send_next_file")
        if Mark.objects.filter(tester=tester, audio__block=tester.current_block).count() >= AudioFiles.objects.filter(block=tester.current_block).count():
            self.bot.send_message(callback.message.chat.id,
                                  f'Ваша ежедневная сессия оценки завершена. Спасибо за проделанную работу. 30 аудиофайлов успешно оценены. Ожидайте следующий набор файлов завтра. Желаем вам приятного вечера!')
            return
        latest_mark = Mark.objects.filter(tester=tester, audio__block=tester.current_block).order_by('-id').first()
        if latest_mark is None:
            latest_mark_audio_id = 0
        else:
            latest_mark_audio_id=latest_mark.audio.id
        print("latest_mark_id: "+str(latest_mark_audio_id))
        next_audio = AudioFiles.objects.filter(id__gt=latest_mark_audio_id, block=tester.current_block, active=True).order_by("name").first()

        if next_audio is None:
            if Mark.objects.filter(tester=tester).count() >= AudioFiles.objects.all().count():
                self.bot.send_message(callback.message.chat.id,
                                  f'Вы успешно завершили все 300 оценок. Спасибо за ваш вклад в это важное исследовательское дело. Мы искренне ценим ваш труд!')
            return

        #self.bot.send_message(callback.message.chat.id,
        #                      f'Ждите файл')

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
                              f'День '+str(tester.current_block)+', исполнитель '+str(next_audio.number)+". Пожалуйста, поставье оценку.",
                              reply_markup=markup)