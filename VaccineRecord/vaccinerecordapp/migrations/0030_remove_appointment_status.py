# Generated by Django 3.2.8 on 2021-11-01 17:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vaccinerecordapp', '0029_alter_appointment_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='appointment',
            name='status',
        ),
    ]