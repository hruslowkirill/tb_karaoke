from django.contrib import admin

# Register your models here.
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse

from core.models import AudioFiles, Tester, Mark, Day, ApplicationQuestion, ApplicationAnswer

from openpyxl import Workbook


@admin.register(AudioFiles)
class AudioFilesAdmin(admin.ModelAdmin):
    list_display = ["created", "modified", "active", "name", "block"]

@admin.register(Tester)
class TesterAdmin(admin.ModelAdmin):
    list_display = ["created", "tg_id", "first_name", "last_name", "username"]

    actions = ("save_to_excel",)

    @admin.action(description='Save to excel')
    def save_to_excel(modeladmin, request, queryset):
        if not request.user.is_staff:
            raise PermissionDenied
        wb = Workbook()
        ws = wb.active
        ws2 = wb.create_sheet("Тестеры")

        field_names = ["audio_id", "audio_name", "block"]
        for tester in queryset:
            field_names.append(tester.id)
        ws.append(field_names)
        audios = AudioFiles.objects.all().order_by("name")
        for a in audios:
            row = [a.id, a.name, a.block]
            for tester in queryset:
                marks = Mark.objects.filter(tester=tester, audio=a)
                if len(marks)>0:
                    row.append(marks[0].value)
                else:
                    row.append("")
            ws.append(row)


        field_names = ["id", "name", "first_name", "last_name", "username"]
        questions = ApplicationQuestion.objects.all().order_by("n")
        for q in questions:
            field_names.append(q.text)
        ws2.append(field_names)
        for tester in queryset:
            row = [tester.id, tester.name, str(tester.first_name), str(tester.last_name), str(tester.username)]
            mm = dict()
            for a in tester.answers.all():
                mm[a.application_questions.id] = a.text
            for q in questions:
                if q.id in mm:
                    row.append(mm[q.id])
                else:
                    row.append("")
            ws2.append(row)



        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f'attachment; filename=marks.xlsx'
        wb.save(response)
        return response

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