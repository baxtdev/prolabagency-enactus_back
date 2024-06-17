import os

from django.core.asgi import get_asgi_application

from channels.security.websocket import AllowedHostsOriginValidator
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter,URLRouter

from apps.chat import routing
from apps.chat.token_auth import TokenAuthMiddleware


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')


application = ProtocolTypeRouter({
    "http":get_asgi_application(),
    'websocket': AllowedHostsOriginValidator(
        TokenAuthMiddleware(
        URLRouter(
            routing.websocket_urlpatterns
        )
    )),
    })