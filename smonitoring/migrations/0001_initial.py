# Generated by Django 3.0.5 on 2020-05-01 12:08

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Poste',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom_poste', models.CharField(max_length=100)),
                ('categorie_poste', models.CharField(max_length=100)),
                ('domaine_poste', models.CharField(max_length=100)),
                ('dept', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Site',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=10, unique=True)),
                ('type_site', models.CharField(max_length=10)),
                ('nom', models.CharField(max_length=100)),
                ('sigle', models.CharField(blank=True, default=None, max_length=10, null=True)),
                ('region', models.CharField(max_length=100)),
                ('departement', models.CharField(max_length=30)),
                ('commune', models.CharField(max_length=100)),
                ('adresse', models.CharField(blank=True, default=None, max_length=100, null=True)),
                ('pepfar', models.CharField(choices=[('oui', 'Oui'), ('non', 'Non')], max_length=10)),
                ('contact_1', models.CharField(max_length=100)),
                ('tel_1', models.CharField(max_length=100)),
                ('contact_2', models.CharField(blank=True, default=None, max_length=100, null=True)),
                ('tel_2', models.CharField(blank=True, default=None, max_length=100, null=True)),
                ('fai', models.CharField(choices=[('digicel', 'Digicel'), ('natcom', 'Natcom'), ('access', 'Access Haiti'), ('hainet', 'Hainet SA')], max_length=100)),
                ('internet', models.CharField(choices=[('up', 'Up'), ('down', 'Down'), ('none', 'Non installe')], max_length=15)),
                ('isante', models.CharField(choices=[('up', 'Up'), ('down', 'Down'), ('none', 'Non installe')], max_length=15)),
                ('fingerprint', models.CharField(choices=[('up', 'Up'), ('down', 'Down'), ('none', 'Non installe')], max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name='Evenement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('entite_concerne', models.CharField(choices=[('internet', 'Internet'), ('isante', 'Isante Server'), ('fingerprint', 'Fingerprint Server')], max_length=100)),
                ('status_ev', models.CharField(choices=[('up', 'Up'), ('down', 'Down'), ('none', 'Non installe')], max_length=10)),
                ('raison_ev', models.CharField(choices=[('0', 'N/A'), ('1', 'Probleme FAI'), ('2', 'Probleme Interne'), ('3', 'Probleme non identifie'), ('4', 'Source non identifie')], max_length=100)),
                ('date_ev', models.DateField(default=datetime.date(2020, 5, 1))),
                ('date_rap', models.DateField(default=datetime.date(2020, 5, 1))),
                ('date_entree', models.DateTimeField(default=datetime.datetime.utcnow)),
                ('pers_contact', models.CharField(max_length=100)),
                ('remarques', models.CharField(max_length=100)),
                ('code_utilisateur', models.CharField(max_length=100)),
                ('code_site', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='site', to='smonitoring.Site')),
            ],
        ),
        migrations.CreateModel(
            name='Employe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code_emp', models.CharField(max_length=100)),
                ('nom', models.CharField(max_length=100)),
                ('prenom', models.CharField(max_length=100)),
                ('email', models.CharField(max_length=100)),
                ('adresse', models.CharField(max_length=100)),
                ('tel_perso', models.CharField(max_length=100)),
                ('tel_travail', models.CharField(max_length=100)),
                ('bureau_affecte', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='smonitoring.Site')),
                ('poste', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='desc_poste', to='smonitoring.Poste')),
            ],
        ),
    ]