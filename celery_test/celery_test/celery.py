from __future__ import absolute_import, unicode_literals
import os
from time import sleep
from uuid import uuid4

from celery import Celery, shared_task
from django.contrib.auth import get_user_model

# from django.contrib.auth.models import User

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'celery_test.settings')

app = Celery('celery_test', broker='redis://localhost/0')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()


@shared_task
def create_users_async(user_count):
    User = get_user_model()
    for i in range(user_count):
        uuid = uuid4()
        1/0
        user = User.objects.create(username=f'user{uuid}')
        print('user_created', user.username)
