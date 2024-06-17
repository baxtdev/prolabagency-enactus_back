# Generated by Django 4.1.7 on 2024-05-15 10:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0005_remove_chatroom_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='Membership',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_admin', models.BooleanField(default=False, verbose_name='Администратор')),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chat.chatroom', verbose_name='комната')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chat.chatuser', verbose_name='пользователь')),
            ],
            options={
                'verbose_name': 'членство в чате',
                'verbose_name_plural': 'членства в чатах',
                'unique_together': {('user', 'room')},
            },
        ),
    ]
