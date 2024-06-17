from urllib import parse

from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware
from django.contrib.auth.models import AnonymousUser
from rest_framework.authtoken.models import Token


class TokenAuthMiddleware(BaseMiddleware):

    def __init__(self, inner):
        super().__init__(inner)

    async def __call__(self, scope, receive, send):
        queries = parse.parse_qs(scope['query_string'].decode())
        if queries.get('Authorization', None) is not None:
            [token_name, token_key] = queries['Authorization'][0].split()
            user = await self._get_user(token_key)
            if user and token_name == 'Token':
                scope['user'] = user
                return await super().__call__(scope, receive, send)
        scope['user'] = AnonymousUser()
        return await super().__call__(scope, receive, send)

    @database_sync_to_async
    def _get_user(self, key):
        try:
            token = Token.objects.get(key=key)
            callable(token.user)
            print("complete user")
            return token.user
        except Token.DoesNotExist as e:
            print("user not found")
            return None