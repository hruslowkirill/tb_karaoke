import os
import glob
from django.core.management import BaseCommand
from core.models import Day
from core.utils import get_today

class Command(BaseCommand):

    def handle(self, *args, **options):
        day = Day(day=get_today(), block=1)
        day.save()
