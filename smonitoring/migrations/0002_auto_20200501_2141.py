# Generated by Django 3.0.5 on 2020-05-01 21:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smonitoring', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='evenement',
            name='pers_contact',
            field=models.CharField(blank=True, default=None, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='evenement',
            name='raison_ev',
            field=models.CharField(choices=[('0', 'N/A'), ('1', 'Problème FAI'), ('2', 'Problème Interne'), ('3', 'Problème non identifie'), ('4', 'Source non identifié')], max_length=100),
        ),
        migrations.AlterField(
            model_name='evenement',
            name='remarques',
            field=models.CharField(blank=True, default=None, max_length=100, null=True),
        ),
    ]
