# Generated by Django 5.0.2 on 2024-05-11 13:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_alter_user_last_activity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='last_activity',
            field=models.DateTimeField(blank=True, null=True, verbose_name='last'),
        ),
    ]
