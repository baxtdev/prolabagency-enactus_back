from django import forms
from django.contrib import admin
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from apps.chat.models import ChatRoom, ChatUser, MessageChat, RequestForSupport,Membership



class MembershipInLine(admin.TabularInline):
    model = Membership
    extra = 0


@admin.register(ChatRoom)
class ChatRoomAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'name',)
    list_filter = ('users',)
    search_fields = ('uuid', 'name',)
    readonly_fields = ('uuid', 'created_at', 'updated_at')
    raw_id_fields = ('users',)


@admin.register(ChatUser)
class UserChatRoomAdmin(admin.ModelAdmin):
    inlines = (MembershipInLine,)
    list_display = ('id', 'name', 'user', 'is_online',)
    list_display_links = ('id', 'name')
    list_filter = ('user',)
    search_fields = ('user__email', 'user__first_name', 'user__last_name')
    readonly_fields = ('created_at', 'updated_at')

    @admin.display(description=_('Аватарка'))
    def get_avatar(self, chat_user):
        if chat_user.avatar:
            return mark_safe(
                f'<img src="{chat_user.avatar.url}" alt="{chat_user.get_full_name}" width="100px" />')
        return '-'


@admin.register(MessageChat)
class MessageChatAdmin(admin.ModelAdmin):
    pass
    # list_display = ('id', 'room', 'type', 'is_read', 'send_notification')
    # list_display_links = ('id', 'room')
    # list_filter = ('room', 'type', 'is_read', 'send_notification', 'chat_user__user')
    # search_fields = ('body', 'room__uuid')
    # raw_id_fields = ('room', 'chat_user')
    # readonly_fields = ('created_at', 'updated_at')


class RequestForSupportAdminForm(forms.ModelForm):
    pass
    # content = forms.CharField(label=_('Текст заявки'), widget=forms.Textarea)

    # class Meta:
    #     model = RequestForSupport
    #     fields = '__all__'


@admin.register(RequestForSupport)
class RequestForSupportAdmin(admin.ModelAdmin):
    pass
    # list_display = ('id', 'header', 'name', 'status')
    # list_display_links = ('id', 'header')
    # list_filter = ('user', 'status')
    # search_fields = ('header', 'name', 'email', 'phone', 'content')
    # readonly_fields = ('created_at', 'updated_at')
    # raw_id_fields = ('user',)
    # form = RequestForSupportAdminForm

# Register your models here.