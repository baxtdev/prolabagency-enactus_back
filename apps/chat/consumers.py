from django.utils import timezone
import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from apps.users.models import User
from apps.chat.models import ChatRoom, MessageChat, ChatUser
from apps.utils.utils import get_object_or_none

SEND_MESSAGE = 'send_message'
MAKE_READ_MESSAGE = 'make_read_message'
TYPING = 'typing'
ONLINE_USER = 'online_user'
NEW_MESSAGE = 'new_message'

class ChatConsumer(AsyncWebsocketConsumer):

    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.room: ChatRoom = None 
        self.user: User = None
        self.room_group: str = None
        self.room_uuid: str = None
        self.handlers = {
            SEND_MESSAGE: self.handle_send_message,
            MAKE_READ_MESSAGE: self.handle_make_read_message,
            TYPING: self.handle_typing
        }

    @database_sync_to_async
    def _get_room(self, uuid):
        try:
            room = ChatRoom.objects.get(uuid=uuid)
            callable(room)
            callable(room.users.all())
            return room
        except ChatRoom.DoesNotExist as e:
            return None

    @database_sync_to_async
    def _get_chat_users(self):
        qs = self.room.users.values('user__id', 'id', 'name', 'user__email')
        return list(qs)

    async def init_validation(self):
        user_ids = [chat_user['user__id'] for chat_user in (await self._get_chat_users())]
        error_codes = {
            4004: self.room is None,
            4001: not self.user.is_authenticated,
            4003: self.user.id not in user_ids
        }

        for code, condition in error_codes.items():
            if condition:
                await self.close(code=code)

    async def connect(self):
        self.room_uuid = self.scope['url_route']['kwargs']['room_uuid']
        self.room_group = f'chat_{self.room_uuid}'
        self.user: User = self.scope['user']
        print(self.scope['user'])
        self.room: ChatRoom = await self._get_room(self.room_uuid)
        await self.init_validation()
        await self.channel_layer.group_add(self.room_group, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group, self.channel_name)

    @database_sync_to_async
    def _save_message(self, body: str, room: ChatRoom, user: User) -> MessageChat:

        chat_user, created = ChatUser.objects.get_or_create(user=user)
        if created:
            chat_user.name = user.get_full_name
            chat_user.avatar = chat_user.avatar
            chat_user = chat_user.save()

        message = MessageChat.objects.create(
            body=body,
            room=room,
            chat_user=chat_user,
        )
        
        callable(message)
        callable(message.chat_user)
        callable(message.chat_user.user)
        callable(message.chat_user.user.image)
        callable(message.room)
        return message

    @property
    def host(self):
        return self.scope.get('headers', [])[0][1].decode('UTF-8', 'ignore')

    @database_sync_to_async
    def _get_to_chat_user(self) -> ChatUser:
        return self.room.users.exclude(user=self.user).first()

    async def receive(self, text_data=None, **kwargs):
        data = json.loads(text_data)
        receive_type = data['type']
        handler = self.handlers[receive_type]
        await handler(data)

    async def notice_new_message(self, message):
        to_chat_user: ChatUser = await self._get_to_chat_user()
        await self.channel_layer.group_send(
            f'online_user_{to_chat_user.id}',
            {
                'type': NEW_MESSAGE,
                'created_at': str(message.created_at),
                'room_uuid': str(self.room.uuid),
                'message_id': message.id,
                'type_message': message.type,
                'chat_user_id': message.chat_user.id,
                'user_id': message.chat_user.user.id
            }
        )

    async def handle_send_message(self, data):
        message: MessageChat = await self._save_message(body=data['body'], room=self.room, user=self.user)
        user = message.chat_user.user
        print(data['body'])
        await self.channel_layer.group_send(
            self.room_group,
            {
                'type': SEND_MESSAGE,
                'body': data['body'],
                'file': None,
                'photo': None,
                'created_at': str(message.created_at),
                'name': message.chat_user.name,
                'type_message': message.type,
                'avatar': f'{self.host}{str(user.image.url)}' if user.image else None,
                'message_id': message.id,
                'chat_user_id': message.chat_user.id,
                'user_id': message.chat_user.user.id
            }
        )

        await self.notice_new_message(message)

    async def send_message(self, event):
        self.room = await self._get_room(self.room_uuid)
        await self.send(text_data=json.dumps(event))

    @database_sync_to_async
    def _make_read_message(self, message_id: int) -> bool:
        message: MessageChat = get_object_or_none(MessageChat, id=message_id)

        if message:

            user_ids = [chat_user.user.id for chat_user in self.room.users.all()]
            user_id = message.chat_user.user.id
            if user_id not in user_ids:
                return False

            message.is_read = True
            message.save()
            return True

        return False

    async def handle_make_read_message(self, data):
        message_id = data['message_id']
        is_read = await self._make_read_message(message_id)
        await self.channel_layer.group_send(
            self.room_group,
            {
                'type': MAKE_READ_MESSAGE,
                'message_id': message_id,
                'is_read': is_read
            }
        )

    async def make_read_message(self, event):
        self.room = await self._get_room(self.room_uuid)
        await self.send(text_data=json.dumps(event))

    async def handle_typing(self, data):
        await self.channel_layer.group_send(
            self.room_group,
            {
                'type': TYPING,
                'chat_user_id': data['chat_user_id'],
                'typing': data['typing']
            }
        )

    async def typing(self, event):
        self.room = await self._get_room(self.room_uuid)
        await self.send(text_data=json.dumps(event))


class OnlineUserConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.chat_user: ChatUser = None
        self.room_group: str = None
        self.user: User = None

    async def init_validation(self):
        error_codes = {
            4001: not self.user.is_authenticated
        }
        for code, condition in error_codes.items():
            if condition:
                await self.close(code=code)

    @database_sync_to_async
    def _get_chat_user(self):
        chat_user = self.user.chat_info
        callable(chat_user.id)
        callable(chat_user.name)
        callable(chat_user.avatar)

        return chat_user

    @database_sync_to_async
    def switch_online(self, value=True):
        self.chat_user.is_online = value
        self.chat_user.save()

    async def connect(self):
        self.user: User = self.scope['user']
        await self.init_validation()
        self.chat_user = await self._get_chat_user()
        await self.chat_user.user._last_activity() 
        await self.switch_online(True)
        self.room_group = f'online_user_{self.chat_user.id}'
        await self.channel_layer.group_add(self.room_group, self.channel_name)
        await self.accept()
        await self.notice_users()

    async def disconnect(self, close_code):
        await self.chat_user.user._last_activity() 
        await self.notice_users(False)
        await self.switch_online(False)
        await self.channel_layer.group_discard(self.room_group, self.channel_name)

    @database_sync_to_async
    def get_chat_user_ids(self):
        to_user_ids = []
        chats = self.user.chat_info.chats.all()
        for chat in chats:
            to_user = chat.users.exclude(id=self.chat_user.id).first()
            to_user_ids.append(to_user.id)
        return to_user_ids

    async def notice_users(self, online=True):
        user_ids = await self.get_chat_user_ids()
        for user_id in user_ids:
            await self.channel_layer.group_send(
                f'online_user_{user_id}',
                {
                    'type': ONLINE_USER,
                    'chat_user_id': self.chat_user.id,
                    'user_id': self.user.id,
                    'is_online': online
                }
            )

    async def online_user(self, event):
        await self.send(text_data=json.dumps(event))

    async def new_message(self, event):
        await self.send(text_data=json.dumps(event))