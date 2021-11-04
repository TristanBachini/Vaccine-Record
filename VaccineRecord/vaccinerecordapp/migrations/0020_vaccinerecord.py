# Generated by Django 3.2.8 on 2021-11-01 10:56

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
            name='VaccineRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bcg_brand', models.CharField(blank=True, max_length=100, null=True)),
                ('bcg_date', models.DateField(null=True)),
                ('bcg_loc', models.CharField(choices=[('R THIGH', 'R thigh'), ('L THIGH', 'L thigh'), ('R ARM', 'R arm'), ('L ARM', 'L arm'), ('R BUTTOCKS', 'R buttocks'), ('L BUTTOCKS', 'L buttocks')], max_length=100, null=True)),
                ('bcg_rem', models.CharField(blank=True, max_length=100, null=True)),
                ('hepb1_brand', models.CharField(blank=True, max_length=100, null=True)),
                ('hepb1_date', models.DateField(null=True)),
                ('hepb1_loc', models.CharField(choices=[('R THIGH', 'R thigh'), ('L THIGH', 'L thigh'), ('R ARM', 'R arm'), ('L ARM', 'L arm'), ('R BUTTOCKS', 'R buttocks'), ('L BUTTOCKS', 'L buttocks')], max_length=100, null=True)),
                ('hepb1_rem', models.CharField(blank=True, max_length=100, null=True)),
                ('hepb2_brand', models.CharField(blank=True, max_length=100, null=True)),
                ('hepb2_date', models.DateField(null=True)),
                ('hepb2_loc', models.CharField(choices=[('R THIGH', 'R thigh'), ('L THIGH', 'L thigh'), ('R ARM', 'R arm'), ('L ARM', 'L arm'), ('R BUTTOCKS', 'R buttocks'), ('L BUTTOCKS', 'L buttocks')], max_length=100, null=True)),
                ('hepb2_rem', models.CharField(blank=True, max_length=100, null=True)),
                ('hepb3_brand', models.CharField(blank=True, max_length=100, null=True)),
                ('hepb3_date', models.DateField(null=True)),
                ('hepb3_loc', models.CharField(choices=[('R THIGH', 'R thigh'), ('L THIGH', 'L thigh'), ('R ARM', 'R arm'), ('L ARM', 'L arm'), ('R BUTTOCKS', 'R buttocks'), ('L BUTTOCKS', 'L buttocks')], max_length=100, null=True)),
                ('hepb3_rem', models.CharField(blank=True, max_length=100, null=True)),
                ('dtap1_brand', models.CharField(blank=True, max_length=100, null=True)),
                ('dtap1_date', models.DateField(null=True)),
                ('dtap1_loc', models.CharField(choices=[('R THIGH', 'R thigh'), ('L THIGH', 'L thigh'), ('R ARM', 'R arm'), ('L ARM', 'L arm'), ('R BUTTOCKS', 'R buttocks'), ('L BUTTOCKS', 'L buttocks')], max_length=100, null=True)),
                ('dtap1_rem', models.CharField(blank=True, max_length=100, null=True)),
                ('dtap2_brand', models.CharField(blank=True, max_length=100, null=True)),
                ('dtap2_date', models.DateField(null=True)),
                ('dtap2_loc', models.CharField(choices=[('R THIGH', 'R thigh'), ('L THIGH', 'L thigh'), ('R ARM', 'R arm'), ('L ARM', 'L arm'), ('R BUTTOCKS', 'R buttocks'), ('L BUTTOCKS', 'L buttocks')], max_length=100, null=True)),
                ('dtap2_rem', models.CharField(blank=True, max_length=100, null=True)),
                ('dtap3_brand', models.CharField(blank=True, max_length=100, null=True)),
                ('dtap3_date', models.DateField(null=True)),
                ('dtap3_loc', models.CharField(choices=[('R THIGH', 'R thigh'), ('L THIGH', 'L thigh'), ('R ARM', 'R arm'), ('L ARM', 'L arm'), ('R BUTTOCKS', 'R buttocks'), ('L BUTTOCKS', 'L buttocks')], max_length=100, null=True)),
                ('dtap3_rem', models.CharField(blank=True, max_length=100, null=True)),
                ('dtap4_brand', models.CharField(blank=True, max_length=100, null=True)),
                ('dtap4_date', models.DateField(null=True)),
                ('dtap4_loc', models.CharField(choices=[('R THIGH', 'R thigh'), ('L THIGH', 'L thigh'), ('R ARM', 'R arm'), ('L ARM', 'L arm'), ('R BUTTOCKS', 'R buttocks'), ('L BUTTOCKS', 'L buttocks')], max_length=100, null=True)),
                ('dtap4_rem', models.CharField(blank=True, max_length=100, null=True)),
                ('dtap5_brand', models.CharField(blank=True, max_length=100, null=True)),
                ('dtap5_date', models.DateField(null=True)),
                ('dtap5_loc', models.CharField(choices=[('R THIGH', 'R thigh'), ('L THIGH', 'L thigh'), ('R ARM', 'R arm'), ('L ARM', 'L arm'), ('R BUTTOCKS', 'R buttocks'), ('L BUTTOCKS', 'L buttocks')], max_length=100, null=True)),
                ('dtap5_rem', models.CharField(blank=True, max_length=100, null=True)),
                ('hib1_brand', models.CharField(blank=True, max_length=100, null=True)),
                ('hib1_date', models.DateField(null=True)),
                ('hib1_loc', models.CharField(choices=[('R THIGH', 'R thigh'), ('L THIGH', 'L thigh'), ('R ARM', 'R arm'), ('L ARM', 'L arm'), ('R BUTTOCKS', 'R buttocks'), ('L BUTTOCKS', 'L buttocks')], max_length=100, null=True)),
                ('hib1_rem', models.CharField(blank=True, max_length=100, null=True)),
                ('hib2_brand', models.CharField(blank=True, max_length=100, null=True)),
                ('hib2_date', models.DateField(null=True)),
                ('hib2_loc', models.CharField(choices=[('R THIGH', 'R thigh'), ('L THIGH', 'L thigh'), ('R ARM', 'R arm'), ('L ARM', 'L arm'), ('R BUTTOCKS', 'R buttocks'), ('L BUTTOCKS', 'L buttocks')], max_length=100, null=True)),
                ('hib2_rem', models.CharField(blank=True, max_length=100, null=True)),
                ('hib3_brand', models.CharField(blank=True, max_length=100, null=True)),
                ('hib3_date', models.DateField(null=True)),
                ('hib3_loc', models.CharField(choices=[('R THIGH', 'R thigh'), ('L THIGH', 'L thigh'), ('R ARM', 'R arm'), ('L ARM', 'L arm'), ('R BUTTOCKS', 'R buttocks'), ('L BUTTOCKS', 'L buttocks')], max_length=100, null=True)),
                ('hib3_rem', models.CharField(blank=True, max_length=100, null=True)),
                ('hib4_brand', models.CharField(blank=True, max_length=100, null=True)),
                ('hib4_date', models.DateField(null=True)),
                ('hib4_loc', models.CharField(choices=[('R THIGH', 'R thigh'), ('L THIGH', 'L thigh'), ('R ARM', 'R arm'), ('L ARM', 'L arm'), ('R BUTTOCKS', 'R buttocks'), ('L BUTTOCKS', 'L buttocks')], max_length=100, null=True)),
                ('hib4_rem', models.CharField(blank=True, max_length=100, null=True)),
                ('hpv11_brand', models.CharField(blank=True, max_length=100, null=True)),
                ('hpv11_date', models.DateField(null=True)),
                ('hpv11_loc', models.CharField(choices=[('R THIGH', 'R thigh'), ('L THIGH', 'L thigh'), ('R ARM', 'R arm'), ('L ARM', 'L arm'), ('R BUTTOCKS', 'R buttocks'), ('L BUTTOCKS', 'L buttocks')], max_length=100, null=True)),
                ('hpv11_rem', models.CharField(blank=True, max_length=100, null=True)),
                ('hpv12_brand', models.CharField(blank=True, max_length=100, null=True)),
                ('hpv12_date', models.DateField(null=True)),
                ('hpv12_loc', models.CharField(choices=[('R THIGH', 'R thigh'), ('L THIGH', 'L thigh'), ('R ARM', 'R arm'), ('L ARM', 'L arm'), ('R BUTTOCKS', 'R buttocks'), ('L BUTTOCKS', 'L buttocks')], max_length=100, null=True)),
                ('hpv12_rem', models.CharField(blank=True, max_length=100, null=True)),
                ('hpv21_brand', models.CharField(blank=True, max_length=100, null=True)),
                ('hpv21_date', models.DateField(null=True)),
                ('hpv21_loc', models.CharField(choices=[('R THIGH', 'R thigh'), ('L THIGH', 'L thigh'), ('R ARM', 'R arm'), ('L ARM', 'L arm'), ('R BUTTOCKS', 'R buttocks'), ('L BUTTOCKS', 'L buttocks')], max_length=100, null=True)),
                ('hpv21_rem', models.CharField(blank=True, max_length=100, null=True)),
                ('hpv22_brand', models.CharField(blank=True, max_length=100, null=True)),
                ('hpv22_date', models.DateField(null=True)),
                ('hpv22_loc', models.CharField(choices=[('R THIGH', 'R thigh'), ('L THIGH', 'L thigh'), ('R ARM', 'R arm'), ('L ARM', 'L arm'), ('R BUTTOCKS', 'R buttocks'), ('L BUTTOCKS', 'L buttocks')], max_length=100, null=True)),
                ('hpv22_rem', models.CharField(blank=True, max_length=100, null=True)),
                ('hpv23_brand', models.CharField(blank=True, max_length=100, null=True)),
                ('hpv23_date', models.DateField(null=True)),
                ('hpv23_loc', models.CharField(choices=[('R THIGH', 'R thigh'), ('L THIGH', 'L thigh'), ('R ARM', 'R arm'), ('L ARM', 'L arm'), ('R BUTTOCKS', 'R buttocks'), ('L BUTTOCKS', 'L buttocks')], max_length=100, null=True)),
                ('hpv23_rem', models.CharField(blank=True, max_length=100, null=True)),
                ('hepa1_brand', models.CharField(blank=True, max_length=100, null=True)),
                ('hepa1_date', models.DateField(null=True)),
                ('hepa1_loc', models.CharField(choices=[('R THIGH', 'R thigh'), ('L THIGH', 'L thigh'), ('R ARM', 'R arm'), ('L ARM', 'L arm'), ('R BUTTOCKS', 'R buttocks'), ('L BUTTOCKS', 'L buttocks')], max_length=100, null=True)),
                ('hepa1_rem', models.CharField(blank=True, max_length=100, null=True)),
                ('hepa2_brand', models.CharField(blank=True, max_length=100, null=True)),
                ('hepa2_date', models.DateField(null=True)),
                ('hepa2_loc', models.CharField(choices=[('R THIGH', 'R thigh'), ('L THIGH', 'L thigh'), ('R ARM', 'R arm'), ('L ARM', 'L arm'), ('R BUTTOCKS', 'R buttocks'), ('L BUTTOCKS', 'L buttocks')], max_length=100, null=True)),
                ('hepa2_rem', models.CharField(blank=True, max_length=100, null=True)),
                ('inf1_brand', models.CharField(blank=True, max_length=100, null=True)),
                ('inf1_date', models.DateField(null=True)),
                ('inf1_loc', models.CharField(choices=[('R THIGH', 'R thigh'), ('L THIGH', 'L thigh'), ('R ARM', 'R arm'), ('L ARM', 'L arm'), ('R BUTTOCKS', 'R buttocks'), ('L BUTTOCKS', 'L buttocks')], max_length=100, null=True)),
                ('inf1_rem', models.CharField(blank=True, max_length=100, null=True)),
                ('inf2_brand', models.CharField(blank=True, max_length=100, null=True)),
                ('inf2_date', models.DateField(null=True)),
                ('inf2_loc', models.CharField(choices=[('R THIGH', 'R thigh'), ('L THIGH', 'L thigh'), ('R ARM', 'R arm'), ('L ARM', 'L arm'), ('R BUTTOCKS', 'R buttocks'), ('L BUTTOCKS', 'L buttocks')], max_length=100, null=True)),
                ('inf2_rem', models.CharField(blank=True, max_length=100, null=True)),
                ('anf_brand', models.CharField(blank=True, max_length=100, null=True)),
                ('anf_date', models.DateField(null=True)),
                ('anf_loc', models.CharField(choices=[('R THIGH', 'R thigh'), ('L THIGH', 'L thigh'), ('R ARM', 'R arm'), ('L ARM', 'L arm'), ('R BUTTOCKS', 'R buttocks'), ('L BUTTOCKS', 'L buttocks')], max_length=100, null=True)),
                ('anf_rem', models.CharField(blank=True, max_length=100, null=True)),
                ('ipv1_brand', models.CharField(blank=True, max_length=100, null=True)),
                ('ipv1_date', models.DateField(null=True)),
                ('ipv1_loc', models.CharField(choices=[('R THIGH', 'R thigh'), ('L THIGH', 'L thigh'), ('R ARM', 'R arm'), ('L ARM', 'L arm'), ('R BUTTOCKS', 'R buttocks'), ('L BUTTOCKS', 'L buttocks')], max_length=100, null=True)),
                ('ipv1_rem', models.CharField(blank=True, max_length=100, null=True)),
                ('ipv2_brand', models.CharField(blank=True, max_length=100, null=True)),
                ('ipv2_date', models.DateField(null=True)),
                ('ipv2_loc', models.CharField(choices=[('R THIGH', 'R thigh'), ('L THIGH', 'L thigh'), ('R ARM', 'R arm'), ('L ARM', 'L arm'), ('R BUTTOCKS', 'R buttocks'), ('L BUTTOCKS', 'L buttocks')], max_length=100, null=True)),
                ('ipv2_rem', models.CharField(blank=True, max_length=100, null=True)),
                ('ipv3_brand', models.CharField(blank=True, max_length=100, null=True)),
                ('ipv3_date', models.DateField(null=True)),
                ('ipv3_loc', models.CharField(choices=[('R THIGH', 'R thigh'), ('L THIGH', 'L thigh'), ('R ARM', 'R arm'), ('L ARM', 'L arm'), ('R BUTTOCKS', 'R buttocks'), ('L BUTTOCKS', 'L buttocks')], max_length=100, null=True)),
                ('ipv3_rem', models.CharField(blank=True, max_length=100, null=True)),
                ('ipv4_brand', models.CharField(blank=True, max_length=100, null=True)),
                ('ipv4_date', models.DateField(null=True)),
                ('ipv4_loc', models.CharField(choices=[('R THIGH', 'R thigh'), ('L THIGH', 'L thigh'), ('R ARM', 'R arm'), ('L ARM', 'L arm'), ('R BUTTOCKS', 'R buttocks'), ('L BUTTOCKS', 'L buttocks')], max_length=100, null=True)),
                ('ipv4_rem', models.CharField(blank=True, max_length=100, null=True)),
                ('ipv5_brand', models.CharField(blank=True, max_length=100, null=True)),
                ('ipv5_date', models.DateField(null=True)),
                ('ipv5_loc', models.CharField(choices=[('R THIGH', 'R thigh'), ('L THIGH', 'L thigh'), ('R ARM', 'R arm'), ('L ARM', 'L arm'), ('R BUTTOCKS', 'R buttocks'), ('L BUTTOCKS', 'L buttocks')], max_length=100, null=True)),
                ('ipv5_rem', models.CharField(blank=True, max_length=100, null=True)),
                ('japb1_brand', models.CharField(blank=True, max_length=100, null=True)),
                ('japb1_date', models.DateField(null=True)),
                ('japb1_loc', models.CharField(choices=[('R THIGH', 'R thigh'), ('L THIGH', 'L thigh'), ('R ARM', 'R arm'), ('L ARM', 'L arm'), ('R BUTTOCKS', 'R buttocks'), ('L BUTTOCKS', 'L buttocks')], max_length=100, null=True)),
                ('japb1_rem', models.CharField(blank=True, max_length=100, null=True)),
                ('japb2_brand', models.CharField(blank=True, max_length=100, null=True)),
                ('japb2_date', models.DateField(null=True)),
                ('japb2_loc', models.CharField(choices=[('R THIGH', 'R thigh'), ('L THIGH', 'L thigh'), ('R ARM', 'R arm'), ('L ARM', 'L arm'), ('R BUTTOCKS', 'R buttocks'), ('L BUTTOCKS', 'L buttocks')], max_length=100, null=True)),
                ('japb2_rem', models.CharField(blank=True, max_length=100, null=True)),
                ('msl_brand', models.CharField(blank=True, max_length=100, null=True)),
                ('msl_date', models.DateField(null=True)),
                ('msl_loc', models.CharField(choices=[('R THIGH', 'R thigh'), ('L THIGH', 'L thigh'), ('R ARM', 'R arm'), ('L ARM', 'L arm'), ('R BUTTOCKS', 'R buttocks'), ('L BUTTOCKS', 'L buttocks')], max_length=100, null=True)),
                ('msl_rem', models.CharField(blank=True, max_length=100, null=True)),
                ('men_brand', models.CharField(blank=True, max_length=100, null=True)),
                ('men_date', models.DateField(null=True)),
                ('men_loc', models.CharField(choices=[('R THIGH', 'R thigh'), ('L THIGH', 'L thigh'), ('R ARM', 'R arm'), ('L ARM', 'L arm'), ('R BUTTOCKS', 'R buttocks'), ('L BUTTOCKS', 'L buttocks')], max_length=100, null=True)),
                ('men_rem', models.CharField(blank=True, max_length=100, null=True)),
                ('mmr1_brand', models.CharField(blank=True, max_length=100, null=True)),
                ('mmr1_date', models.DateField(null=True)),
                ('mmr1_loc', models.CharField(choices=[('R THIGH', 'R thigh'), ('L THIGH', 'L thigh'), ('R ARM', 'R arm'), ('L ARM', 'L arm'), ('R BUTTOCKS', 'R buttocks'), ('L BUTTOCKS', 'L buttocks')], max_length=100, null=True)),
                ('mmr1_rem', models.CharField(blank=True, max_length=100, null=True)),
                ('mmr2_brand', models.CharField(blank=True, max_length=100, null=True)),
                ('mmr2_date', models.DateField(null=True)),
                ('mmr2_loc', models.CharField(choices=[('R THIGH', 'R thigh'), ('L THIGH', 'L thigh'), ('R ARM', 'R arm'), ('L ARM', 'L arm'), ('R BUTTOCKS', 'R buttocks'), ('L BUTTOCKS', 'L buttocks')], max_length=100, null=True)),
                ('mmr2_rem', models.CharField(blank=True, max_length=100, null=True)),
                ('pcv1_brand', models.CharField(blank=True, max_length=100, null=True)),
                ('pcv1_date', models.DateField(null=True)),
                ('pcv1_loc', models.CharField(choices=[('R THIGH', 'R thigh'), ('L THIGH', 'L thigh'), ('R ARM', 'R arm'), ('L ARM', 'L arm'), ('R BUTTOCKS', 'R buttocks'), ('L BUTTOCKS', 'L buttocks')], max_length=100, null=True)),
                ('pcv1_rem', models.CharField(blank=True, max_length=100, null=True)),
                ('pcv2_brand', models.CharField(blank=True, max_length=100, null=True)),
                ('pcv2_date', models.DateField(null=True)),
                ('pcv2_loc', models.CharField(choices=[('R THIGH', 'R thigh'), ('L THIGH', 'L thigh'), ('R ARM', 'R arm'), ('L ARM', 'L arm'), ('R BUTTOCKS', 'R buttocks'), ('L BUTTOCKS', 'L buttocks')], max_length=100, null=True)),
                ('pcv2_rem', models.CharField(blank=True, max_length=100, null=True)),
                ('pcv3_brand', models.CharField(blank=True, max_length=100, null=True)),
                ('pcv3_date', models.DateField(null=True)),
                ('pcv3_loc', models.CharField(choices=[('R THIGH', 'R thigh'), ('L THIGH', 'L thigh'), ('R ARM', 'R arm'), ('L ARM', 'L arm'), ('R BUTTOCKS', 'R buttocks'), ('L BUTTOCKS', 'L buttocks')], max_length=100, null=True)),
                ('pcv3_rem', models.CharField(blank=True, max_length=100, null=True)),
                ('pcv4_brand', models.CharField(blank=True, max_length=100, null=True)),
                ('pcv4_date', models.DateField(null=True)),
                ('pcv4_loc', models.CharField(choices=[('R THIGH', 'R thigh'), ('L THIGH', 'L thigh'), ('R ARM', 'R arm'), ('L ARM', 'L arm'), ('R BUTTOCKS', 'R buttocks'), ('L BUTTOCKS', 'L buttocks')], max_length=100, null=True)),
                ('pcv4_rem', models.CharField(blank=True, max_length=100, null=True)),
                ('rota1_brand', models.CharField(blank=True, max_length=100, null=True)),
                ('rota1_date', models.DateField(null=True)),
                ('rota1_loc', models.CharField(choices=[('R THIGH', 'R thigh'), ('L THIGH', 'L thigh'), ('R ARM', 'R arm'), ('L ARM', 'L arm'), ('R BUTTOCKS', 'R buttocks'), ('L BUTTOCKS', 'L buttocks')], max_length=100, null=True)),
                ('rota1_rem', models.CharField(blank=True, max_length=100, null=True)),
                ('rota2_brand', models.CharField(blank=True, max_length=100, null=True)),
                ('rota2_date', models.DateField(null=True)),
                ('rota2_loc', models.CharField(choices=[('R THIGH', 'R thigh'), ('L THIGH', 'L thigh'), ('R ARM', 'R arm'), ('L ARM', 'L arm'), ('R BUTTOCKS', 'R buttocks'), ('L BUTTOCKS', 'L buttocks')], max_length=100, null=True)),
                ('rota2_rem', models.CharField(blank=True, max_length=100, null=True)),
                ('rota3_brand', models.CharField(blank=True, max_length=100, null=True)),
                ('rota3_date', models.DateField(null=True)),
                ('rota3_loc', models.CharField(choices=[('R THIGH', 'R thigh'), ('L THIGH', 'L thigh'), ('R ARM', 'R arm'), ('L ARM', 'L arm'), ('R BUTTOCKS', 'R buttocks'), ('L BUTTOCKS', 'L buttocks')], max_length=100, null=True)),
                ('rota3_rem', models.CharField(blank=True, max_length=100, null=True)),
                ('td_brand', models.CharField(blank=True, max_length=100, null=True)),
                ('td_date', models.DateField(null=True)),
                ('td_loc', models.CharField(choices=[('R THIGH', 'R thigh'), ('L THIGH', 'L thigh'), ('R ARM', 'R arm'), ('L ARM', 'L arm'), ('R BUTTOCKS', 'R buttocks'), ('L BUTTOCKS', 'L buttocks')], max_length=100, null=True)),
                ('td_rem', models.CharField(blank=True, max_length=100, null=True)),
                ('typ_brand', models.CharField(blank=True, max_length=100, null=True)),
                ('typ_date', models.DateField(null=True)),
                ('typ_loc', models.CharField(choices=[('R THIGH', 'R thigh'), ('L THIGH', 'L thigh'), ('R ARM', 'R arm'), ('L ARM', 'L arm'), ('R BUTTOCKS', 'R buttocks'), ('L BUTTOCKS', 'L buttocks')], max_length=100, null=True)),
                ('typ_rem', models.CharField(blank=True, max_length=100, null=True)),
                ('var1_brand', models.CharField(blank=True, max_length=100, null=True)),
                ('var1_date', models.DateField(null=True)),
                ('var1_loc', models.CharField(choices=[('R THIGH', 'R thigh'), ('L THIGH', 'L thigh'), ('R ARM', 'R arm'), ('L ARM', 'L arm'), ('R BUTTOCKS', 'R buttocks'), ('L BUTTOCKS', 'L buttocks')], max_length=100, null=True)),
                ('var1_rem', models.CharField(blank=True, max_length=100, null=True)),
                ('var2_brand', models.CharField(blank=True, max_length=100, null=True)),
                ('var2_date', models.DateField(null=True)),
                ('var2_loc', models.CharField(choices=[('R THIGH', 'R thigh'), ('L THIGH', 'L thigh'), ('R ARM', 'R arm'), ('L ARM', 'L arm'), ('R BUTTOCKS', 'R buttocks'), ('L BUTTOCKS', 'L buttocks')], max_length=100, null=True)),
                ('var2_rem', models.CharField(blank=True, max_length=100, null=True)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
