# Generated by Django 3.2.8 on 2021-11-01 13:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vaccinerecordapp', '0022_auto_20211101_2046'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vaccine',
            name='anf_loc',
            field=models.CharField(blank=True, choices=[('R THIGH', 'R thigh'), ('L THIGH', 'L thigh'), ('R ARM', 'R arm'), ('L ARM', 'L arm'), ('R BUTTOCKS', 'R buttocks'), ('L BUTTOCKS', 'L buttocks')], max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='vaccine',
            name='bcg_loc',
            field=models.CharField(blank=True, choices=[('R THIGH', 'R thigh'), ('L THIGH', 'L thigh'), ('R ARM', 'R arm'), ('L ARM', 'L arm'), ('R BUTTOCKS', 'R buttocks'), ('L BUTTOCKS', 'L buttocks')], max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='vaccine',
            name='dtap1_loc',
            field=models.CharField(blank=True, choices=[('R THIGH', 'R thigh'), ('L THIGH', 'L thigh'), ('R ARM', 'R arm'), ('L ARM', 'L arm'), ('R BUTTOCKS', 'R buttocks'), ('L BUTTOCKS', 'L buttocks')], max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='vaccine',
            name='dtap2_loc',
            field=models.CharField(blank=True, choices=[('R THIGH', 'R thigh'), ('L THIGH', 'L thigh'), ('R ARM', 'R arm'), ('L ARM', 'L arm'), ('R BUTTOCKS', 'R buttocks'), ('L BUTTOCKS', 'L buttocks')], max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='vaccine',
            name='dtap3_loc',
            field=models.CharField(blank=True, choices=[('R THIGH', 'R thigh'), ('L THIGH', 'L thigh'), ('R ARM', 'R arm'), ('L ARM', 'L arm'), ('R BUTTOCKS', 'R buttocks'), ('L BUTTOCKS', 'L buttocks')], max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='vaccine',
            name='dtap4_loc',
            field=models.CharField(blank=True, choices=[('R THIGH', 'R thigh'), ('L THIGH', 'L thigh'), ('R ARM', 'R arm'), ('L ARM', 'L arm'), ('R BUTTOCKS', 'R buttocks'), ('L BUTTOCKS', 'L buttocks')], max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='vaccine',
            name='dtap5_loc',
            field=models.CharField(blank=True, choices=[('R THIGH', 'R thigh'), ('L THIGH', 'L thigh'), ('R ARM', 'R arm'), ('L ARM', 'L arm'), ('R BUTTOCKS', 'R buttocks'), ('L BUTTOCKS', 'L buttocks')], max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='vaccine',
            name='hepa1_loc',
            field=models.CharField(blank=True, choices=[('R THIGH', 'R thigh'), ('L THIGH', 'L thigh'), ('R ARM', 'R arm'), ('L ARM', 'L arm'), ('R BUTTOCKS', 'R buttocks'), ('L BUTTOCKS', 'L buttocks')], max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='vaccine',
            name='hepa2_loc',
            field=models.CharField(blank=True, choices=[('R THIGH', 'R thigh'), ('L THIGH', 'L thigh'), ('R ARM', 'R arm'), ('L ARM', 'L arm'), ('R BUTTOCKS', 'R buttocks'), ('L BUTTOCKS', 'L buttocks')], max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='vaccine',
            name='hepb1_loc',
            field=models.CharField(blank=True, choices=[('R THIGH', 'R thigh'), ('L THIGH', 'L thigh'), ('R ARM', 'R arm'), ('L ARM', 'L arm'), ('R BUTTOCKS', 'R buttocks'), ('L BUTTOCKS', 'L buttocks')], max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='vaccine',
            name='hepb2_loc',
            field=models.CharField(blank=True, choices=[('R THIGH', 'R thigh'), ('L THIGH', 'L thigh'), ('R ARM', 'R arm'), ('L ARM', 'L arm'), ('R BUTTOCKS', 'R buttocks'), ('L BUTTOCKS', 'L buttocks')], max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='vaccine',
            name='hepb3_loc',
            field=models.CharField(blank=True, choices=[('R THIGH', 'R thigh'), ('L THIGH', 'L thigh'), ('R ARM', 'R arm'), ('L ARM', 'L arm'), ('R BUTTOCKS', 'R buttocks'), ('L BUTTOCKS', 'L buttocks')], max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='vaccine',
            name='hib1_loc',
            field=models.CharField(blank=True, choices=[('R THIGH', 'R thigh'), ('L THIGH', 'L thigh'), ('R ARM', 'R arm'), ('L ARM', 'L arm'), ('R BUTTOCKS', 'R buttocks'), ('L BUTTOCKS', 'L buttocks')], max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='vaccine',
            name='hib2_loc',
            field=models.CharField(blank=True, choices=[('R THIGH', 'R thigh'), ('L THIGH', 'L thigh'), ('R ARM', 'R arm'), ('L ARM', 'L arm'), ('R BUTTOCKS', 'R buttocks'), ('L BUTTOCKS', 'L buttocks')], max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='vaccine',
            name='hib3_loc',
            field=models.CharField(blank=True, choices=[('R THIGH', 'R thigh'), ('L THIGH', 'L thigh'), ('R ARM', 'R arm'), ('L ARM', 'L arm'), ('R BUTTOCKS', 'R buttocks'), ('L BUTTOCKS', 'L buttocks')], max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='vaccine',
            name='hib4_loc',
            field=models.CharField(blank=True, choices=[('R THIGH', 'R thigh'), ('L THIGH', 'L thigh'), ('R ARM', 'R arm'), ('L ARM', 'L arm'), ('R BUTTOCKS', 'R buttocks'), ('L BUTTOCKS', 'L buttocks')], max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='vaccine',
            name='hpv11_loc',
            field=models.CharField(blank=True, choices=[('R THIGH', 'R thigh'), ('L THIGH', 'L thigh'), ('R ARM', 'R arm'), ('L ARM', 'L arm'), ('R BUTTOCKS', 'R buttocks'), ('L BUTTOCKS', 'L buttocks')], max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='vaccine',
            name='hpv12_loc',
            field=models.CharField(blank=True, choices=[('R THIGH', 'R thigh'), ('L THIGH', 'L thigh'), ('R ARM', 'R arm'), ('L ARM', 'L arm'), ('R BUTTOCKS', 'R buttocks'), ('L BUTTOCKS', 'L buttocks')], max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='vaccine',
            name='hpv21_loc',
            field=models.CharField(blank=True, choices=[('R THIGH', 'R thigh'), ('L THIGH', 'L thigh'), ('R ARM', 'R arm'), ('L ARM', 'L arm'), ('R BUTTOCKS', 'R buttocks'), ('L BUTTOCKS', 'L buttocks')], max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='vaccine',
            name='hpv22_loc',
            field=models.CharField(blank=True, choices=[('R THIGH', 'R thigh'), ('L THIGH', 'L thigh'), ('R ARM', 'R arm'), ('L ARM', 'L arm'), ('R BUTTOCKS', 'R buttocks'), ('L BUTTOCKS', 'L buttocks')], max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='vaccine',
            name='hpv23_loc',
            field=models.CharField(blank=True, choices=[('R THIGH', 'R thigh'), ('L THIGH', 'L thigh'), ('R ARM', 'R arm'), ('L ARM', 'L arm'), ('R BUTTOCKS', 'R buttocks'), ('L BUTTOCKS', 'L buttocks')], max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='vaccine',
            name='inf1_loc',
            field=models.CharField(blank=True, choices=[('R THIGH', 'R thigh'), ('L THIGH', 'L thigh'), ('R ARM', 'R arm'), ('L ARM', 'L arm'), ('R BUTTOCKS', 'R buttocks'), ('L BUTTOCKS', 'L buttocks')], max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='vaccine',
            name='inf2_loc',
            field=models.CharField(blank=True, choices=[('R THIGH', 'R thigh'), ('L THIGH', 'L thigh'), ('R ARM', 'R arm'), ('L ARM', 'L arm'), ('R BUTTOCKS', 'R buttocks'), ('L BUTTOCKS', 'L buttocks')], max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='vaccine',
            name='ipv1_loc',
            field=models.CharField(blank=True, choices=[('R THIGH', 'R thigh'), ('L THIGH', 'L thigh'), ('R ARM', 'R arm'), ('L ARM', 'L arm'), ('R BUTTOCKS', 'R buttocks'), ('L BUTTOCKS', 'L buttocks')], max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='vaccine',
            name='ipv2_loc',
            field=models.CharField(blank=True, choices=[('R THIGH', 'R thigh'), ('L THIGH', 'L thigh'), ('R ARM', 'R arm'), ('L ARM', 'L arm'), ('R BUTTOCKS', 'R buttocks'), ('L BUTTOCKS', 'L buttocks')], max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='vaccine',
            name='ipv3_loc',
            field=models.CharField(blank=True, choices=[('R THIGH', 'R thigh'), ('L THIGH', 'L thigh'), ('R ARM', 'R arm'), ('L ARM', 'L arm'), ('R BUTTOCKS', 'R buttocks'), ('L BUTTOCKS', 'L buttocks')], max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='vaccine',
            name='ipv4_loc',
            field=models.CharField(blank=True, choices=[('R THIGH', 'R thigh'), ('L THIGH', 'L thigh'), ('R ARM', 'R arm'), ('L ARM', 'L arm'), ('R BUTTOCKS', 'R buttocks'), ('L BUTTOCKS', 'L buttocks')], max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='vaccine',
            name='ipv5_loc',
            field=models.CharField(blank=True, choices=[('R THIGH', 'R thigh'), ('L THIGH', 'L thigh'), ('R ARM', 'R arm'), ('L ARM', 'L arm'), ('R BUTTOCKS', 'R buttocks'), ('L BUTTOCKS', 'L buttocks')], max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='vaccine',
            name='japb1_loc',
            field=models.CharField(blank=True, choices=[('R THIGH', 'R thigh'), ('L THIGH', 'L thigh'), ('R ARM', 'R arm'), ('L ARM', 'L arm'), ('R BUTTOCKS', 'R buttocks'), ('L BUTTOCKS', 'L buttocks')], max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='vaccine',
            name='japb2_loc',
            field=models.CharField(blank=True, choices=[('R THIGH', 'R thigh'), ('L THIGH', 'L thigh'), ('R ARM', 'R arm'), ('L ARM', 'L arm'), ('R BUTTOCKS', 'R buttocks'), ('L BUTTOCKS', 'L buttocks')], max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='vaccine',
            name='men_loc',
            field=models.CharField(blank=True, choices=[('R THIGH', 'R thigh'), ('L THIGH', 'L thigh'), ('R ARM', 'R arm'), ('L ARM', 'L arm'), ('R BUTTOCKS', 'R buttocks'), ('L BUTTOCKS', 'L buttocks')], max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='vaccine',
            name='mmr1_loc',
            field=models.CharField(blank=True, choices=[('R THIGH', 'R thigh'), ('L THIGH', 'L thigh'), ('R ARM', 'R arm'), ('L ARM', 'L arm'), ('R BUTTOCKS', 'R buttocks'), ('L BUTTOCKS', 'L buttocks')], max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='vaccine',
            name='mmr2_loc',
            field=models.CharField(blank=True, choices=[('R THIGH', 'R thigh'), ('L THIGH', 'L thigh'), ('R ARM', 'R arm'), ('L ARM', 'L arm'), ('R BUTTOCKS', 'R buttocks'), ('L BUTTOCKS', 'L buttocks')], max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='vaccine',
            name='msl_loc',
            field=models.CharField(blank=True, choices=[('R THIGH', 'R thigh'), ('L THIGH', 'L thigh'), ('R ARM', 'R arm'), ('L ARM', 'L arm'), ('R BUTTOCKS', 'R buttocks'), ('L BUTTOCKS', 'L buttocks')], max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='vaccine',
            name='pcv1_loc',
            field=models.CharField(blank=True, choices=[('R THIGH', 'R thigh'), ('L THIGH', 'L thigh'), ('R ARM', 'R arm'), ('L ARM', 'L arm'), ('R BUTTOCKS', 'R buttocks'), ('L BUTTOCKS', 'L buttocks')], max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='vaccine',
            name='pcv2_loc',
            field=models.CharField(blank=True, choices=[('R THIGH', 'R thigh'), ('L THIGH', 'L thigh'), ('R ARM', 'R arm'), ('L ARM', 'L arm'), ('R BUTTOCKS', 'R buttocks'), ('L BUTTOCKS', 'L buttocks')], max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='vaccine',
            name='pcv3_loc',
            field=models.CharField(blank=True, choices=[('R THIGH', 'R thigh'), ('L THIGH', 'L thigh'), ('R ARM', 'R arm'), ('L ARM', 'L arm'), ('R BUTTOCKS', 'R buttocks'), ('L BUTTOCKS', 'L buttocks')], max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='vaccine',
            name='pcv4_loc',
            field=models.CharField(blank=True, choices=[('R THIGH', 'R thigh'), ('L THIGH', 'L thigh'), ('R ARM', 'R arm'), ('L ARM', 'L arm'), ('R BUTTOCKS', 'R buttocks'), ('L BUTTOCKS', 'L buttocks')], max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='vaccine',
            name='rota1_loc',
            field=models.CharField(blank=True, choices=[('R THIGH', 'R thigh'), ('L THIGH', 'L thigh'), ('R ARM', 'R arm'), ('L ARM', 'L arm'), ('R BUTTOCKS', 'R buttocks'), ('L BUTTOCKS', 'L buttocks')], max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='vaccine',
            name='rota2_loc',
            field=models.CharField(blank=True, choices=[('R THIGH', 'R thigh'), ('L THIGH', 'L thigh'), ('R ARM', 'R arm'), ('L ARM', 'L arm'), ('R BUTTOCKS', 'R buttocks'), ('L BUTTOCKS', 'L buttocks')], max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='vaccine',
            name='rota3_loc',
            field=models.CharField(blank=True, choices=[('R THIGH', 'R thigh'), ('L THIGH', 'L thigh'), ('R ARM', 'R arm'), ('L ARM', 'L arm'), ('R BUTTOCKS', 'R buttocks'), ('L BUTTOCKS', 'L buttocks')], max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='vaccine',
            name='td_loc',
            field=models.CharField(blank=True, choices=[('R THIGH', 'R thigh'), ('L THIGH', 'L thigh'), ('R ARM', 'R arm'), ('L ARM', 'L arm'), ('R BUTTOCKS', 'R buttocks'), ('L BUTTOCKS', 'L buttocks')], max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='vaccine',
            name='typ_loc',
            field=models.CharField(blank=True, choices=[('R THIGH', 'R thigh'), ('L THIGH', 'L thigh'), ('R ARM', 'R arm'), ('L ARM', 'L arm'), ('R BUTTOCKS', 'R buttocks'), ('L BUTTOCKS', 'L buttocks')], max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='vaccine',
            name='var1_loc',
            field=models.CharField(blank=True, choices=[('R THIGH', 'R thigh'), ('L THIGH', 'L thigh'), ('R ARM', 'R arm'), ('L ARM', 'L arm'), ('R BUTTOCKS', 'R buttocks'), ('L BUTTOCKS', 'L buttocks')], max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='vaccine',
            name='var2_loc',
            field=models.CharField(blank=True, choices=[('R THIGH', 'R thigh'), ('L THIGH', 'L thigh'), ('R ARM', 'R arm'), ('L ARM', 'L arm'), ('R BUTTOCKS', 'R buttocks'), ('L BUTTOCKS', 'L buttocks')], max_length=100, null=True),
        ),
    ]