# Generated by Django 5.0.2 on 2024-05-11 13:16

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0001_initial'),
        ('university', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='university',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='university.university', verbose_name='Университет команды'),
            preserve_default=False,
        ),
    ]
