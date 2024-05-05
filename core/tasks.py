from celery import shared_task

from core.models import Day
from core.utils import get_today

@shared_task
def start_new_day():
    # Task logic here
    block = 1
    days = Day.objects.all().order_by("-id")
    if len(days) != 0:
        block = days[0].block+1
    day = Day()
    day.day = get_today()
    day.block = block
    day.save()