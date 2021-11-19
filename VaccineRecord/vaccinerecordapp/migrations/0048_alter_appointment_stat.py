# Generated by Django 3.2.6 on 2021-11-05 16:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vaccinerecordapp', '0047_merge_0028_alter_vaccine_patient_no_0046_vaccine'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='stat',
            field=models.CharField(choices=[('CONFIRMED', 'Confirmed'), ('UNCONFIRMED', 'Unconfirmed'), ('POSTPONED', 'Postponed')], max_length=11),
        ),
    ]