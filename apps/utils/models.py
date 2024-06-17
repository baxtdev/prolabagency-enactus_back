from django.db import models
from django.utils.translation import gettext_lazy as _
from django.db.utils import IntegrityError

class TimeStampAbstractModel(models.Model):
    created_at = models.DateTimeField(_('дата добавления'), auto_now_add=True)
    updated_at = models.DateTimeField(_('дата изменения'), auto_now=True)

    class Meta:
        abstract = True



class SoccialNetworks(models.Model):
    instagram_url = models.URLField(
        _("Инстаграм"),
        blank=True,	
        null=True,
        max_length=255,
    )
    twitter_url = models.URLField(
        _("Твиттер"),
        blank=True,
        null=True,
        max_length=255,
    )
    tik_tok_url = models.URLField(
        _("ТикТок"),
        blank=True,
        null=True,
        max_length=255,
    )
    facebook_url = models.URLField(
        _("Фейсбук"),
        blank=True,
        null=True,
        max_length=255,
    )
    youtube_url = models.URLField(
        _("Ютуб"),
        blank=True,
        null=True,
        max_length=255,
    )
    telegram_url = models.URLField(
        _("Телеграм"),
        blank=True,
        null=True,
        max_length=255,
    )

    class Meta:
        abstract = True



def _get_chat_user(user,model):
    chat_user,created = model.objects.get_or_create(user=user)
    if created:
            chat_user.avatar = user.image
            if user.get_full_name is None: 
                chat_user.name = user.email.split('@')[0]
            else:
                chat_user.name = user.get_full_name     
            chat_user.save()
    return chat_user        


def create_admin(chat_user,model,room):
    try:
        membership = model.objects.create(user=chat_user,room=room,is_admin=True)
        return membership
    except IntegrityError:
        return None