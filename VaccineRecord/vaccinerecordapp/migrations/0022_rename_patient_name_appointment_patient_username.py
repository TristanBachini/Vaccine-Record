# Generated by Django 3.2.8 on 2021-11-01 12:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vaccinerecordapp', '0021_auto_20211101_1230'),
    ]

    operations = [
        migrations.RenameField(
            model_name='appointment',
            old_name='patient_name',
            new_name='patient_username',
        ),
    ]