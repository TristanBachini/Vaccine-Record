# Generated by Django 3.2.8 on 2021-11-01 11:01

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('vaccinerecordapp', '0020_vaccinerecord'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='VaccineRecord',
            new_name='Vaccine',
        ),
    ]
