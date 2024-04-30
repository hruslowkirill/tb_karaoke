from django.core.management import BaseCommand
from core.models import ApplicationQuestion, ApplicationAnswer

class Command(BaseCommand):

    def handle(self, *args, **options):
        print("load_questions")

        q = ApplicationQuestion(n=1, text="Ваш пол")
        q.save()
        ApplicationAnswer.objects.create(text="Мужчина", application_questions=q)
        ApplicationAnswer.objects.create(text="Женщина", application_questions=q)

        q = ApplicationQuestion(n=2, text="Возраст")
        q.save()
        ApplicationAnswer.objects.create(text="18-24", application_questions=q)
        ApplicationAnswer.objects.create(text="25-34", application_questions=q)
        ApplicationAnswer.objects.create(text="35-44", application_questions=q)
        ApplicationAnswer.objects.create(text="45-54", application_questions=q)
        ApplicationAnswer.objects.create(text="55-64", application_questions=q)
        ApplicationAnswer.objects.create(text="65+", application_questions=q)

        q = ApplicationQuestion(n=3, text="Как Вы считаете, есть ли у Вас музыкальный слух?")
        q.save()
        ApplicationAnswer.objects.create(text="Да", application_questions=q)
        ApplicationAnswer.objects.create(text="Скорее да, чем нет", application_questions=q)
        ApplicationAnswer.objects.create(text="Скорее нет, чем да", application_questions=q)
        ApplicationAnswer.objects.create(text="Нет", application_questions=q)

        q = ApplicationQuestion(n=4, text="Поете ли Вы для себя?")
        q.save()
        ApplicationAnswer.objects.create(text="Всегда что-то напеваю", application_questions=q)
        ApplicationAnswer.objects.create(text="Иногда (дома, в ванной, в машине и т.д.)", application_questions=q)
        ApplicationAnswer.objects.create(text="Очень редко", application_questions=q)
        ApplicationAnswer.objects.create(text="Нет, не пою", application_questions=q)

        q = ApplicationQuestion(n=5, text="Вы поете на публике?")
        q.save()
        ApplicationAnswer.objects.create(text="Выступаю или выступал(а) на сцене", application_questions=q)
        ApplicationAnswer.objects.create(text="Выкладываю или выкладывал(а) видео с пением в соцсетях", application_questions=q)
        ApplicationAnswer.objects.create(text="Пою иногда для друзей или гостей, в караоке", application_questions=q)
        ApplicationAnswer.objects.create(text="Нет, не пою", application_questions=q)

        q = ApplicationQuestion(n=6, text="Как, по мнению Ваших друзей, знакомых, близких, Вы поете?")
        q.save()
        ApplicationAnswer.objects.create(text="Очень хорошо", application_questions=q)
        ApplicationAnswer.objects.create(text="Хорошо", application_questions=q)
        ApplicationAnswer.objects.create(text="Обычно, как большинство", application_questions=q)
        ApplicationAnswer.objects.create(text="Наверное, считают, что плохо", application_questions=q)

        q = ApplicationQuestion(n=7, text="Как часто Вы слушаете музыку?")
        q.save()
        ApplicationAnswer.objects.create(text="Часто, почти каждый день", application_questions=q)
        ApplicationAnswer.objects.create(text="Слушаю, но не каждый день", application_questions=q)
        ApplicationAnswer.objects.create(text="Редко", application_questions=q)

        q = ApplicationQuestion(n=8, text="Играете ли Вы на каких-либо музыкальных инструментах?")
        q.save()
        ApplicationAnswer.objects.create(text="Да, играю", application_questions=q)
        ApplicationAnswer.objects.create(text="Имею небольшие навыки", application_questions=q)
        ApplicationAnswer.objects.create(text="Нет", application_questions=q)

        q = ApplicationQuestion(n=9, text="Занимались или занимаетесь ли Вы вокалом?")
        q.save()
        ApplicationAnswer.objects.create(text="Да", application_questions=q)
        ApplicationAnswer.objects.create(text="Как-то пробовал(а) / хочу попробовать", application_questions=q)
        ApplicationAnswer.objects.create(text="Нет", application_questions=q)

        q = ApplicationQuestion(n=10, text="Имеете ли Вы музыкальное образование?")
        q.save()
        ApplicationAnswer.objects.create(text="Высшее музыкальное образование", application_questions=q)
        ApplicationAnswer.objects.create(text="Музыкальная школа", application_questions=q)
        ApplicationAnswer.objects.create(text="Нет", application_questions=q)

        q = ApplicationQuestion(n=11, text="Что для Вас музыка?")
        q.save()
        ApplicationAnswer.objects.create(text="Часть моей профессии", application_questions=q)
        ApplicationAnswer.objects.create(text="Мое хобби, которому уделяю много времени", application_questions=q)
        ApplicationAnswer.objects.create(text="Способ выражения чувств и эмоций", application_questions=q)
        ApplicationAnswer.objects.create(text="Просто музыка", application_questions=q)