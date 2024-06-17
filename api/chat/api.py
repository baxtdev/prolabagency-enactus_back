from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.utils.translation import gettext_lazy as _
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status
from rest_framework.generics import GenericAPIView, get_object_or_404, CreateAPIView,UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.mixins import UltraReadOnlyModelViewSet, QuerySetByUserMixin, UltraModelViewSet,ModelViewSet
from apps.users.models import User
from apps.chat.consumers import SEND_MESSAGE, NEW_MESSAGE
from apps.chat.models import ChatRoom, ChatUser, MessageChat, RequestForSupport
from .permissions import IsOwnerForChatRoom, IsOwnerForMessageChat
from .serializers import ReadChatRoomSerializer, ReadUserChatSerializer, ReadMessageChatSerializer, \
    CreateChatRoomSerializer, CreatGeneralChatRoomsSerializer,UploadFileByMessageSerializer, ReadRequestForSupportSerializer, \
    CreateRequestForSupportSerializer, RequestForSupportSerializer,Membership,CreateMembershipSerializer,ReadGeneralChatRoomsSerializer
from ..pagination import StandardResultsSetPagination, MediumResultsSetPagination
from ..permissions import IsSuperAdmin, IsOwner


class ChatRoomViewSet(UltraReadOnlyModelViewSet):
    queryset = ChatRoom.objects.all()
    serializer_classes = {
        'list': ReadChatRoomSerializer,
        'retrieve': ReadChatRoomSerializer,
    }
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend,
                       filters.OrderingFilter,
                       filters.SearchFilter]
    ordering_fields = ['created_at']
    search_fields = ['name', 'uuid', 'users__name', 'users__user__email', 'users__user__last_name',
                    'users__user__first_name']
    filterset_fields = ['users', 'users__user','room_type']
    permission_classes_by_action = {
        'list': (IsAuthenticated,),
        'retrieve': (IsAuthenticated, IsOwnerForChatRoom),
    }

    def get_queryset(self):
        qs = super().get_queryset()
        user: User = self.request.user
        if user.is_authenticated:
            if not user.is_superuser:
                return qs.filter(users__user=user)
        return qs



class AddAdminToGeneralChatViewSet(ModelViewSet):
    serializer_class = CreateMembershipSerializer
    queryset = Membership.objects.all()


class CreateChatRoomApiView(CreateAPIView,):
    serializer_class = CreateChatRoomSerializer
    permission_classes = (IsAuthenticated,)



class CreateGeneralChatRoomApiView(UltraModelViewSet):
    serializer_class = CreatGeneralChatRoomsSerializer
    permission_classes = (IsAuthenticated,)
    queryset = ChatRoom.objects.all()
    
    serializer_classes = {
        'list': ReadGeneralChatRoomsSerializer,
        'retrieve': ReadGeneralChatRoomsSerializer,
        'create': CreatGeneralChatRoomsSerializer,
        'update': CreatGeneralChatRoomsSerializer,
        'partial_update': CreatGeneralChatRoomsSerializer,
        'destroy': CreatGeneralChatRoomsSerializer,
    }
    permission_classes_by_action = {
        'list': (IsAuthenticated,),
        'retrieve': (IsAuthenticated, IsOwnerForChatRoom),
    }

    # def get_queryset(self):
    #     qs = super().get_queryset()
    #     user: User = self.request.user
    #     if user.is_authenticated:
    #         if not user.is_superuser:
    #             return qs.filter(created_by=user)
    #     return qs


class UserChatViewSet(UltraReadOnlyModelViewSet, QuerySetByUserMixin):
    queryset = ChatUser.objects.all()
    serializer_classes = {
        'list': ReadUserChatSerializer,
        'retrieve': ReadUserChatSerializer,
    }
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend,
                       filters.OrderingFilter,
                       filters.SearchFilter]
    ordering_fields = ['created_at']
    search_fields = ['name', 'user__email', 'user__first_name', 'user__last_name']
    filterset_fields = ['user']
    permission_classes_by_action = {
        'list': (IsAuthenticated,),
        'retrieve': (IsAuthenticated, IsOwner),
    }


class MessageChatViewSet(UltraReadOnlyModelViewSet):
    queryset = MessageChat.objects.all()
    serializer_classes = {
        'list': ReadMessageChatSerializer,
        'retrieve': ReadMessageChatSerializer,
    }
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend,
                       filters.OrderingFilter,
                       filters.SearchFilter]
    ordering_fields = ['created_at']
    search_fields = ['room__name', 'room__uuid', 'body']
    filterset_fields = ['chat_user', 'room', 'chat_user__user', 'type', 'is_read', 'send_notification']
    permission_classes_by_action = {
        'list': (IsAuthenticated, IsSuperAdmin),
        'retrieve': (IsAuthenticated, IsOwnerForMessageChat),
    }


class MessagesByRoomChatApiView(GenericAPIView):
    queryset = MessageChat.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = ReadMessageChatSerializer
    pagination_class = MediumResultsSetPagination

    def get(self, request, uuid, *args, **kwargs):
        chat_room = get_object_or_404(ChatRoom, uuid=uuid)
        if request.user.chat_info in chat_room.users.all():
            queryset = self.filter_queryset(self.get_queryset().filter(room=chat_room))

            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data[::-1])

            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data[::-1])
        return Response(
            {'detail': _(f'Вы не можете получить чужие сообщения.')},
            status=status.HTTP_403_FORBIDDEN
        )


class UploadFileByMessageApiView(GenericAPIView):
    queryset = ChatRoom.objects.all()
    lookup_field = 'uuid'
    permission_classes = (IsAuthenticated, IsOwnerForChatRoom)
    serializer_class = UploadFileByMessageSerializer

    def post(self, request, *args, **kwargs):
        chat_room: ChatRoom = self.get_object()
        try:
            chat_user = request.user.chat_info
        except ChatUser.DoesNotExist:
            return Response({'detail': _('Пользователь не имеет настройку чата.')}, status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        message: MessageChat = serializer.save(
            room=chat_room,
            chat_user=chat_user
        )
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f'chat_{chat_room.uuid}',
            {
                'type': SEND_MESSAGE,
                'body': message.body,
                'file': request.build_absolute_uri(message.file.url) if message.file else None,
                'photo': request.build_absolute_uri(message.photo.url) if message.photo else None,
                'created_at': str(message.created_at),
                'name': message.chat_user.name,
                'type_message': message.type,
                'avatar': message.chat_user.user.image.url if message.chat_user.user.image else None,
                'chat_user_id': message.chat_user.id,
                'user_id': message.chat_user.user.id
            }
        )
        to_chat_user: ChatUser = chat_room.users.exclude(user=request.user).first()
        async_to_sync(channel_layer.group_send)(
            f'online_user_{to_chat_user.id}',
            {
                'type': NEW_MESSAGE,
                'created_at': str(message.created_at),
                'room_uuid': str(chat_room.uuid),
                'message_id': message.id,
                'type_message': message.type,
                'chat_user_id': message.chat_user.id,
                'user_id': message.chat_user.user.id
            }
        )
        return Response({'detail': 'Файл успешно загружен.'})


class RequestForSupportViewSet(UltraModelViewSet, QuerySetByUserMixin):
    queryset = RequestForSupport.objects.all()
    serializer_classes = {
        'list': ReadRequestForSupportSerializer,
        'retrieve': ReadRequestForSupportSerializer,
        'create': CreateRequestForSupportSerializer,
        'update': RequestForSupportSerializer,
    }
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend,
                       filters.OrderingFilter,
                       filters.SearchFilter]
    ordering_fields = ['created_at']
    search_fields = ['header', 'name', 'email', 'phone', 'content']
    filterset_fields = ['user', 'status']
    permission_classes_by_action = {
        'list': (IsAuthenticated,),
        'retrieve': (IsAuthenticated, IsOwner),
        'create': (IsAuthenticated,),
        'update': (IsAuthenticated, IsSuperAdmin),
        'destroy': (IsAuthenticated, IsSuperAdmin),
    }


class CloseRequestForSupportApiView(GenericAPIView):
    queryset = RequestForSupport.objects.all()
    lookup_field = 'id'
    permission_classes = (IsAuthenticated, IsOwner)

    def get(self, request, *args, **kwargs):
        request_for_support: RequestForSupport = self.get_object()
        if request_for_support.status != RequestForSupport.CLOSED:
            return Response({'detail': _('Заявка уже закрыто')}, status.HTTP_400_BAD_REQUEST)
        request_for_support.status = RequestForSupport.CLOSED
        request_for_support.save()
        return Response({'detail': _('Заявка успешно закрыто клиентом.')})