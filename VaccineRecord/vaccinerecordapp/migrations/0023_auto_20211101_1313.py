# Generated by Django 3.2.8 on 2021-11-01 13:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vaccinerecordapp', '0022_rename_patient_name_appointment_patient_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='location',
            field=models.CharField(choices=[('MANILA', 'Manila'), ('MAKATI', 'Makati')], max_length=6),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='time',
            field=models.CharField(choices=[('9:00', '9:00 AM'), ('9:30', '9:30 AM'), ('10:00', '10:00 AM'), ('10:30', '10:30 AM'), ('11:00', '11:00 AM'), ('11:30', '11:30 AM'), ('12:00', '12:00 PM'), ('12:30', '12:30 PM')], max_length=5),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='visit',
            field=models.CharField(choices=[('V', 'Vaccine'), ('AC', 'Annual Checkup')], max_length=2),
        ),
        migrations.DeleteModel(
            name='Location',
        ),
        migrations.DeleteModel(
            name='Time',
        ),
        migrations.DeleteModel(
            name='Visit',
        ),
    ]