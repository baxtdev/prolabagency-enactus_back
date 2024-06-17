from django.db.models import Q
from django.db import transaction

from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from apps.users.models import User
from apps.chat.models import ChatRoom, ChatUser, MessageChat, RequestForSupport,Membership
from apps.utils.serializers import ShortDescUserSerializer
from apps.utils.models import _get_chat_user,create_admin

class UserChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatUser
        fields = '__all__'



class ReadRolesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Membership
        fields = ('id','is_admin')   


class ReadUserChatSerializer(serializers.ModelSerializer):
    user = ShortDescUserSerializer()
    is_owner = serializers.SerializerMethodField('validate_is_owner')
    # roles = ReadRolesSerializer(many=True)
    class Meta:
        model = ChatUser
        fields = '__all__'


    def validate_is_owner(self, obj):
        return obj.user == self.context['request'].user


class ChatRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatRoom
        fields = '__all__'


class ReadMembershipSerializer(serializers.ModelSerializer):
    user = ReadUserChatSerializer()
    class Meta:
        model = Membership
        fields = '__all__'


class CreateMembershipSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Membership
        fields = '__all__'



class CreatGeneralChatRoomsSerializer(serializers.ModelSerializer):
    users = serializers.PrimaryKeyRelatedField(many=True, queryset=User.objects.all())

    class Meta:
        model = ChatRoom
        fields = ('uuid','name','users')
    @transaction.atomic
    def create(self, validated_data):
        chat_users = []
        
        users = validated_data.pop('users',None) 
        user = self.context['request'].user

        admin_user = _get_chat_user(user,ChatUser)
        chat_users.append(admin_user)

        room: ChatRoom = super().create(validated_data)

        for user in users:
            chat_user = _get_chat_user(user,ChatUser)
            chat_users.append(chat_user)
        
        room.users.add(*chat_users)
        room.created_by = admin_user
        room.room_type = ChatRoom.GROUP_GENERAL
        admin = create_admin(admin_user,Membership,room,)
        room.save()
        return room

    def update(self, instance, validated_data):
        room = super().update(instance, validated_data)
        user = self.context['request'].user
        admin_user = _get_chat_user(user,ChatUser)
        room.users.add(admin_user)

        return room



class ReadGeneralChatRoomsSerializer(serializers.ModelSerializer):
    users = ReadUserChatSerializer(many=True)
    unread_messages = serializers.SerializerMethodField('get_unread_messages')
    admins = ReadMembershipSerializer(many=True)

    class Meta:
        model = ChatRoom
        fields = '__all__'

    def get_unread_messages(self, chat_room: ChatRoom) -> int:
        user: User = self.context['request'].user
        return chat_room.unread_messages(user)    



class ReadChatRoomSerializer(serializers.ModelSerializer):
    users = ReadUserChatSerializer(many=True)
    unread_messages = serializers.SerializerMethodField('get_unread_messages')
    class Meta:
        model = ChatRoom
        fields = '__all__'
        
    def get_unread_messages(self, chat_room: ChatRoom) -> int:
        user: User = self.context['request'].user
        return chat_room.unread_messages(user)


class MessageChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = MessageChat
        fields = '__all__'


class ReadMessageChatSerializer(serializers.ModelSerializer):
    chat_user = ReadUserChatSerializer()
    room = ChatRoomSerializer()

    class Meta:
        model = MessageChat
        fields = '__all__'


class CreateChatRoomSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), write_only=True)
    uuid = serializers.UUIDField(read_only=True)
    users = ReadUserChatSerializer(many=True, read_only=True)

    class Meta:
        model = ChatRoom
        fields = ('name', 'user', 'users', 'uuid')
    
    @transaction.atomic
    def create(self, validated_data):
        request = self.context['request']
        user, to_user = request.user, validated_data.pop('user')
        if user == to_user:
            raise serializers.ValidationError({'user': [
                _(f'Пользователь "{user.get_full_name}" не может открыть чат сам собой.')
            ]})
        users = ChatRoom.objects.filter(users__user=user).filter(users__user=to_user).filter(room_type=ChatRoom.PERSONAL)
        if users.exists():
            raise serializers.ValidationError({'user': [
                _(f'Пользователь "{user.get_full_name}" уже имеет совместный чат с "{to_user.get_full_name}".')
            ]})

        room: ChatRoom = super().create(validated_data)

        users = []
        for user_item in [user, to_user]:
            chat_user = _get_chat_user(user=user_item,model=ChatUser)
            users.append(chat_user)

        room.users.add(*users)
        return room


class UploadFileByMessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = MessageChat
        fields = ('photo', 'file')

    def validate(self, attrs):
        photo = attrs.get('photo')
        file = attrs.get('file')

        if not file and not photo:
            raise serializers.ValidationError({'photo': [_('Нужно заполнить один из полей.')]})

        return attrs


class RequestForSupportSerializer(serializers.ModelSerializer):

    class Meta:
        model = RequestForSupport
        fields = '__all__'


class ReadRequestForSupportSerializer(serializers.ModelSerializer):
    user = ShortDescUserSerializer()

    class Meta:
        model = RequestForSupport
        fields = '__all__'


class CreateRequestForSupportSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequestForSupport
        exclude = ('user', 'status')

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data.setdefault('user', user)
        return super().create(validated_data)