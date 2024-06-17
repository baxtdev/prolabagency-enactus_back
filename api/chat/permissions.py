from django.http import HttpRequest
from rest_framework.permissions import BasePermission

from apps.chat.models import ChatRoom, MessageChat


class IsOwnerForChatRoom(BasePermission):

    def has_object_permission(self, request: HttpRequest, view, obj: ChatRoom):
        return request.user in obj.users.all() or request.user.is_superuser


class IsOwnerForMessageChat(BasePermission):
    def has_object_permission(self, request: HttpRequest, view, obj: MessageChat):
        return request.user in obj.room.users.all() or request.user.is_superuser