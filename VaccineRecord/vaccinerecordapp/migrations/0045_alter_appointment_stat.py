# Generated by Django 3.2.8 on 2021-11-01 18:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vaccinerecordapp', '0044_auto_20211101_1816'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='stat',
            field=models.CharField(choices=[('Confirmed', 'Confirmed'), ('Unconfirmed', 'Unconfirmed'), ('Postponed', 'Postponed')], max_length=11),
        ),
    ]
