from uuid import uuid4

from celery import shared_task
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from celery_test.celery import create_users_async, send_email_async
from celery_test.logdna import log
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=User)
def email_handler(sender, **kwargs):
    send_email_async.delay()


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()

    @action(methods=['post'], detail=False)
    def create_users(self, request):
        is_async = request.data['is_async']
        user_counts = request.data['user_count']

        if is_async:
            create_users_async.delay(user_counts)
            log.info('async_true')

        else:
            create_users_async(user_counts)
            # Simplest use case
            log.info('async_false')

            # Add a custom level
            log.info('로그', {'level': '중요'})

            # Include an App name with this specific log
            log.info('노우!!!!!', {'level': 'Warn', 'app': 'users'})

        return Response(data={'user_count': user_counts}, status=status.HTTP_201_CREATED)

    @action(methods=['post'], detail=False)
    def create_user_email(self, request):
        """유저 생성시 이메일 전송"""
        User = get_user_model()
        uuid = uuid4()
        user = User.objects.create(username=f'user{uuid}')
        print('user_created', user.username)

        return Response(data={'username': user.username}, status=status.HTTP_201_CREATED)
