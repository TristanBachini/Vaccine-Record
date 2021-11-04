# Generated by Django 3.2.8 on 2021-11-01 13:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vaccinerecordapp', '0023_auto_20211101_1313'),
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
        migrations.AlterField(
            model_name='appointment',
            name='location',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='vaccinerecordapp.location'),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='time',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='vaccinerecordapp.time'),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='visit',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='vaccinerecordapp.visit'),
        ),
    ]
