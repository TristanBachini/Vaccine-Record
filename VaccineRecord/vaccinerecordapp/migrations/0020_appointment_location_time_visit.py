# Generated by Django 3.2.6 on 2021-11-01 11:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('vaccinerecordapp', '0019_auto_20211019_2249'),
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location', models.CharField(max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Time',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.CharField(max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Visit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('visit', models.CharField(max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('patient_name', models.CharField(blank=True, max_length=100, null=True)),
                ('status', models.CharField(blank=True, max_length=100, null=True)),
                ('date', models.DateTimeField(null=True)),
                ('time', models.CharField(blank=True, max_length=100, null=True)),
                ('doctor', models.CharField(blank=True, max_length=100, null=True)),
                ('visit', models.CharField(blank=True, max_length=100, null=True)),
                ('location', models.CharField(blank=True, max_length=100, null=True)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]