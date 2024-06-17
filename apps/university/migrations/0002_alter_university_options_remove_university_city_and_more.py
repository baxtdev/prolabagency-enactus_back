# Generated by Django 4.1.7 on 2024-05-13 13:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('regions', '0001_initial'),
        ('university', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='university',
            options={'managed': True, 'ordering': ['id', 'name'], 'verbose_name': 'Университет', 'verbose_name_plural': 'Университеты'},
        ),
        migrations.RemoveField(
            model_name='university',
            name='city',
        ),
        migrations.AddField(
            model_name='university',
            name='region',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='regions.region', verbose_name='Регион'),
        ),
    ]
