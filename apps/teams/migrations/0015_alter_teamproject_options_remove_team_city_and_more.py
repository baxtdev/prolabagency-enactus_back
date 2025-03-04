# Generated by Django 4.1.7 on 2024-05-13 13:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('regions', '0001_initial'),
        ('teams', '0014_teammembers_departament'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='teamproject',
            options={'managed': True, 'ordering': ['id', 'name'], 'verbose_name': 'Проект Команды', 'verbose_name_plural': 'Проекты Команд'},
        ),
        migrations.RemoveField(
            model_name='team',
            name='city',
        ),
        migrations.RemoveField(
            model_name='teamproject',
            name='city',
        ),
        migrations.AddField(
            model_name='team',
            name='region',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='regions.region', verbose_name='Регион'),
        ),
        migrations.AddField(
            model_name='teamproject',
            name='region',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='regions.region', verbose_name='Регион'),
        ),
    ]
