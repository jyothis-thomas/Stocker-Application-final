# Generated by Django 2.2.5 on 2019-10-15 12:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quotes', '0006_ticker'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ticker',
            new_name='TickerModel',
        ),
    ]
