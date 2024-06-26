from __future__ import absolute_import

import os

from celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tb_karaoke.settings")

app = Celery("tb_karaoke")

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object("django.conf:settings", namespace="CELERY")
#app.conf.timezone = 'Asia/Yekaterinburg'
app.autodiscover_tasks()