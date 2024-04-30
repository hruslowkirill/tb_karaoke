from django.contrib import admin

# Register your models here.
from core.models import AudioFiles, Tester, Mark, Day, ApplicationQuestion, ApplicationAnswer


@admin.register(AudioFiles)
class AudioFilesAdmin(admin.ModelAdmin):
    list_display = ["created", "modified", "active", "name", "block"]

@admin.register(Tester)
class TesterAdmin(admin.ModelAdmin):
    list_display = ["created", "tg_id", "first_name", "last_name", "username"]

@admin.register(Mark)
class MarkAdmin(admin.ModelAdmin):
    list_display = ["created", "tester", "audio", "day", "value"]

@admin.register(Day)
class DayAdmin(admin.ModelAdmin):
    list_display = ["created", "day", "block"]

@admin.register(ApplicationQuestion)
class ApplicationQuestionAdmin(admin.ModelAdmin):
    list_display = ["created", "n", "text"]

@admin.register(ApplicationAnswer)
class ApplicationAnswerAdmin(admin.ModelAdmin):
    list_display = ["created", "text", "application_questions"]