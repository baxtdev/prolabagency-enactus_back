from django.db.models.signals import post_save,post_migrate
from django.dispatch import receiver

from apps.utils.utils import send_code
from core.settings import FRONTENT_REGISTRATION_URL
from .models import InvitationToMembers

@receiver(post_save,sender=InvitationToMembers)
def send_invitation_email(sender,instance:InvitationToMembers,created,**kwargs):
    text = f"""Здаравствуйте {instance.first_name}!  
            Вы приглашены в команду {instance.team},пригласил вас {instance.invited_by} чтобы принять приглашение перехиде по ссылку
            {FRONTENT_REGISTRATION_URL}{instance.token}
            """
    if created:
        resp = send_code(text,instance.email,"Приглашение в команду Enactus")
        print(resp)
