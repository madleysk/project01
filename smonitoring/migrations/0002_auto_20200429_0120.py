# Generated by Django 3.0.5 on 2020-04-29 01:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smonitoring', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='site',
            name='adresse',
            field=models.CharField(blank=True, default=None, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='site',
            name='contact_2',
            field=models.CharField(blank=True, default=None, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='site',
            name='sigle',
            field=models.CharField(blank=True, default=None, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='site',
            name='tel_2',
            field=models.CharField(blank=True, default=None, max_length=100, null=True),
        ),
    ]
