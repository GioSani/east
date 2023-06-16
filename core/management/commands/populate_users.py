from django.core.management import BaseCommand
from django.db import connections
from django.db.utils import OperationalError
import time

from faker import Faker

from core.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        #faker = Faker()
        users = User.objects.using('old').all()[:5]
        #print('======',user)
        for user in users:
            user_ = User.objects.create(
                first_name=user.first_name,
                last_name=user.last_name,
                email=user.email,
                password='',
                is_ambassador=True
            )
            user_.set_password('1234')
            user_.save()
            print(f'{user_.first_name} == saved')
