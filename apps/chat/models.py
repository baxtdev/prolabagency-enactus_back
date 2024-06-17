from uuid import uuid4

from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.utils.models import TimeStampAbstractModel

from phonenumber_field.modelfields import PhoneNumberField

from django_resized import ResizedImageField


class Membership(models.Model):
    user = models.ForeignKey('ChatUser', on_delete=models.CASCADE, verbose_name=_('пользователь'),related_name='roles')
    room = models.ForeignKey('ChatRoom', on_delete=models.CASCADE, verbose_name=_('комната'),related_name="admins")
    is_admin = models.BooleanField(_('Администратор'), default=False)

    class Meta:
        verbose_name = _('членство в чате')
        verbose_name_plural = _('членства в чатах')
        unique_together = ('user', 'room')  

    def __str__(self):
        return f'{self.user.name} - {self.room.name} - Admin: {self.is_admin}'



class ChatRoom(TimeStampAbstractModel):
    GROUP_GENERAL = 'group_general'
    PERSONAL = 'personal'

    ROOM_TYPES = (
        (GROUP_GENERAL, _('Групповая общая')),
        (PERSONAL, _('Личная')),
    )
    created_by = models.ForeignKey('chat.ChatUser',models.SET_NULL,related_name='chat_groups',null=True,blank=True)
    room_type = models.CharField(_('тип комнаты'), choices=ROOM_TYPES, default=PERSONAL, max_length=50)
    uuid = models.UUIDField(_('идентификационный ключ'), unique=True, default=uuid4, primary_key=True, editable=False)
    name = models.CharField(_('название комнаты'), max_length=150)
    users = models.ManyToManyField('chat.ChatUser', 'chats', verbose_name=_('пользователи'))

    class Meta:
        verbose_name = _('комната чата')
        verbose_name_plural = _('комната чатов')
        ordering = ('-created_at', '-updated_at')

    def __str__(self):
        return f'{self.uuid}: {self.name}'

    def unread_messages(self, user):
        return self.messages.exclude(chat_user=user.chat_info).filter(is_read=False).count()


class ChatUser(TimeStampAbstractModel):
    user = models.OneToOneField('users.User', models.SET_NULL, related_name='chat_info', verbose_name=_('пользователь'), null=True)
    is_online = models.BooleanField(_('В сети'), default=False)
    name = models.CharField(_('имя пользователя'), max_length=100, null=True)
    avatar = ResizedImageField(size=[500, 500], crop=['middle', 'center'],
                               upload_to='chat_avatars/', force_format='WEBP', quality=90, verbose_name=_('аватарка'),
                               null=True, blank=True)

    class Meta:
        verbose_name = _('пользователь чата')
        verbose_name_plural = _('пользователи чата')
        ordering = ('-created_at', '-updated_at')

    def __str__(self):
        return f'{self.name} - {self.user.id}'


def message_photo_upload_path(instance, filename):
    user_email = instance.chat_user.user.email if instance.chat_user is not None else 'announcement'
    return f'chats/{instance.room.uuid}/{user_email}/photos/{filename}'


def message_file_upload_path(instance, filename):
    user_email = instance.chat_user.user.email if instance.chat_user is not None else 'announcement'
    return f'chats/{instance.room.uuid}/{user_email}/files/{filename}'


class MessageChat(TimeStampAbstractModel):
    SIMPLE = 'simple'
    ANNOUNCEMENT = 'announcement'

    TYPES = (
        (SIMPLE, _('Обычный')),
        (ANNOUNCEMENT, _('Объявление'))
    )

    class Meta:
        verbose_name = _('сообщение')
        verbose_name_plural = _('сообщении')
        ordering = ('-created_at',)

    body = models.TextField(_('сообщение'), null=True, blank=True)
    photo = ResizedImageField(_('фото'), upload_to=message_photo_upload_path, quality=90, force_format='WEBP',
                              blank=True, null=True)
    file = models.FileField(_('файл'), upload_to=message_file_upload_path, blank=True, null=True)
    type = models.CharField(_('тип'), choices=TYPES, default=SIMPLE,max_length=50)
    chat_user = models.ForeignKey('chat.ChatUser', models.CASCADE, 'messages', blank=True, null=True,
                                  verbose_name=_('пользователь'))
    room = models.ForeignKey('chat.ChatRoom', models.CASCADE, 'messages', verbose_name=_('комната'))
    is_read = models.BooleanField(_('прочитано'), default=False)
    send_notification = models.BooleanField(_('Отправить уведомление о сообщений'), default=False)

    def __str__(self):
        return f'{self.chat_user} - {self.room.uuid}'


def request_for_support_upload_path(instance, filename):
    return f'request_for_supports/{instance.email}/{filename}'

class RequestForSupport(TimeStampAbstractModel):

    WAITING = 'waiting'
    ACCEPTED = 'accepted'
    CLOSED = 'closed'

    STATUS = (
        (WAITING, _('В ожидании')),
        (ACCEPTED, _('Принято')),
        (CLOSED, _('Закрыто'))
    )

    class Meta:
        verbose_name = _('заявка на тех. поддержку')
        verbose_name_plural = _('заявки на тех. поддержку')
        ordering = ('-created_at', '-updated_at')

    header = models.CharField(_('тема заявки'), max_length=255)
    name = models.CharField(_('имя и фамилия'), max_length=255)
    email = models.EmailField(_('ваш контактный e-mail'))
    phone = PhoneNumberField(_('ваш контактный телефон'))
    content = models.CharField(_('текст заявки'), max_length=2000)
    file = models.FileField(_('файл'), upload_to=request_for_support_upload_path, null=True, blank=True)
    status = models.CharField(_('статус'), choices=STATUS, default=WAITING, max_length=20)
    user = models.ForeignKey('users.User', models.SET_NULL, null=True, verbose_name=_('пользователь'))

    def __str__(self):
        return f'{self.name} - {self.header}'