from django.core.management import BaseCommand
from django.db import connections
from django.db.utils import OperationalError
from django.contrib.auth.models import Group
import time

from faker import Faker

from core.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        faker = Faker()

        for _ in range(30):

            if _ < 10:
                management_group = Group.objects.get(name='management')  
                print('group==',management_group)
                user = User.objects.create(
                

                first_name=faker.first_name(),
                last_name=faker.last_name(),
                email=faker.email(),
                password='',
                is_ambassador=True,
                is_management = True,
                )
                user.set_password('1234')
                #user.groups.set([group])
                user.groups.add(management_group)
                print('faker users===',user)

                user.save()
