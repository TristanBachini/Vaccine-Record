# Generated by Django 3.2.6 on 2021-10-12 00:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vaccinerecordapp', '0004_alter_doctor_contact'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctor',
            name='contact',
            field=models.CharField(max_length=100),
        ),
    ]
