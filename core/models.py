import os
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django_extensions.db.models import TimeStampedModel
# Create your models here.


class AudioFiles(TimeStampedModel):
    class Meta:
        verbose_name = "Аудио файл"
        verbose_name_plural = "Аудио файлы"
        ordering = ["-created"]

    name =  models.CharField(max_length=64)
    active = models.BooleanField()
    file = models.FileField(upload_to ='media/uploads/')
    block = models.PositiveSmallIntegerField(default=0)
    number = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return os.path.basename(self.file.name)

class ApplicationQuestion(TimeStampedModel):
    class Meta:
        verbose_name = "Вопрос"
        verbose_name_plural = "Вопросы"
        ordering = ["created"]

    n = models.PositiveSmallIntegerField(default=0)
    text = models.CharField(max_length=256)

    def __str__(self):
        return self.text


class ApplicationAnswer(TimeStampedModel):
    class Meta:
        verbose_name = "Ответ"
        verbose_name_plural = "Ответы"
        ordering = ["-created"]

    application_questions = models.ForeignKey(ApplicationQuestion, null=False, on_delete=models.RESTRICT, related_name="answers")
    text = models.CharField(max_length=256)


class Tester(TimeStampedModel):
    class Meta:
        verbose_name = "Тестер"
        verbose_name_plural = "Тестеры"
        ordering = ["-created"]

    name = models.CharField(max_length=64, null=True)
    first_name = models.CharField(max_length=64, null=True)
    last_name = models.CharField(max_length=64, null=True)
    username = models.CharField(max_length=64, null=True)
    tg_id = models.PositiveBigIntegerField()
    answers = models.ManyToManyField(ApplicationAnswer)
    last_question = models.PositiveSmallIntegerField(default=0)
    chat_id = models.CharField(max_length=32, default=0)
    current_block = models.IntegerField(default=1)

    def __str__(self):
        return str(self.username)+" "+str(self.tg_id)+" "+str(self.name)


class Mark(TimeStampedModel):
    class Meta:
        verbose_name = "Оценка"
        verbose_name_plural = "Оценки"
        ordering = ["-created"]
        unique_together = ('tester', 'audio',)

    tester = models.ForeignKey(Tester, null=False, on_delete=models.RESTRICT, related_name="marks")
    audio = models.ForeignKey(AudioFiles, null=False, on_delete=models.RESTRICT, related_name="marks")
    audio_message_id = models.PositiveIntegerField(default=0)
    value = models.PositiveSmallIntegerField()


class ErrorLog(TimeStampedModel):
    class Meta:
        verbose_name = "Лог ошибки"
        verbose_name_plural = "Логи ошибки"
        ordering = ["-created"]

    tester = models.ForeignKey(Tester, null=True, on_delete=models.RESTRICT, related_name="error_logs")
    audio = models.ForeignKey(AudioFiles, null=True, on_delete=models.RESTRICT, related_name="error_logs")
    type = models.CharField(max_length=32, null=False)
    description = models.TextField(null=False)
    second_description = models.TextField(null=True)
    success_resend = models.BooleanField(default=False)


