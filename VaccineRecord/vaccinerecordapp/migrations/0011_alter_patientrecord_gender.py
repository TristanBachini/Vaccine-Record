# Generated by Django 3.2.8 on 2021-10-16 06:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vaccinerecordapp', '0010_alter_patientrecord_gender'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patientrecord',
            name='gender',
            field=models.CharField(choices=[('MALE', 'Male'), ('FEMALE', 'Female')], max_length=11, null=True),
        ),
    ]
