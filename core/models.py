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

class Tester(TimeStampedModel):
    class Meta:
        verbose_name = "Тестер"
        verbose_name_plural = "Тестеры"
        ordering = ["-created"]

    first_name =  models.CharField(max_length=64, null=True)
    last_name = models.CharField(max_length=64, null=True)
    username = models.CharField(max_length=64, null=True)
    tg_id = models.PositiveBigIntegerField()

class Mark(TimeStampedModel):
    class Meta:
        verbose_name = "Оценка"
        verbose_name_plural = "Оценки"
        ordering = ["-created"]

    tester = models.ForeignKey(Tester, null=False, on_delete=models.RESTRICT, related_name="marks")
    audio = models.ForeignKey(AudioFiles, null=False, on_delete=models.RESTRICT, related_name="marks")
    value = models.PositiveSmallIntegerField()