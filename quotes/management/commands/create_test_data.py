from django.contrib.auth.models import User
from movieapp.models import MotionPicture as mp
from django.utils import timezone
from django.core.files import File
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Creates User and Movies'
    def handle(self, *args, **kwargs):

        ad = User(username='admin')
        ad.set_password('admin')
        ad.email = 'admin@email.com'
        ad.is_staff = True
        ad.is_superuser = True
        ad.save()
        self.stdout.write("User Created {}".format(ad.username))

        test1 = User(username='test1')
        test1.set_password('asdf')
        test1.email = 'test1@email.com'
        test1.is_active = True
        test1.save()
        self.stdout.write("User Created {}".format(test1.username))

        test2 = User(username='test2')
        test2.set_password('asdf')
        test2.email = 'test2@email.com'
        test2.is_active = True
        test2.save()
        self.stdout.write("User Created {}".format(test2.username))




