from django.contrib import admin

# Register your models here.
from core.models import AudioFiles, Tester, Mark, Day


@admin.register(AudioFiles)
class AudioFilesAdmin(admin.ModelAdmin):
    list_display = ["created", "modified", "active", "name"]

@admin.register(Tester)
class TesterAdmin(admin.ModelAdmin):
    list_display = ["created", "tg_id", "first_name", "last_name", "username"]

@admin.register(Mark)
class MarkAdmin(admin.ModelAdmin):
    list_display = ["created", "tester", "audio", "day", "value"]

@admin.register(Day)
class DayAdmin(admin.ModelAdmin):
    list_display = ["created", "day"]