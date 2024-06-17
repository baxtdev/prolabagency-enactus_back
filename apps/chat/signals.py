from django.db.models.signals import post_save,post_migrate,pre_save
from django.dispatch import receiver

from .models import ChatRoom,MessageChat


@receiver(pre_save,sender=ChatRoom)
def send_invitation_email(sender,instance:ChatRoom,**kwargs):
    if instance.room_type == ChatRoom.GROUP_GENERAL:
        message = MessageChat.objects.create(
            body=f'Пользователь {instance.created_by.name} создал чат ',
            room=instance,
            chat_user=instance.created_by,
            type=MessageChat.ANNOUNCEMENT
        )
            