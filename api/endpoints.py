from rest_framework import routers
from django.urls import include, path

from .yasg import urlpatterns as url_doc
from .auth.endpoints import urlpatterns as auth_urls
from .users.endpoints import urlpatterns as users_urls
from .chat.endpoints import urlpatterns as cha_urls
from .university.endpoints import urlpatterns as university_urls
from .teams.endpoints import urlpatterns as teams_url
from .enactus.endpoints import urlpatterns as enactus_urls


urlpatterns=[
    path('accounts/', include(auth_urls)),
    path('',include(users_urls)),
    path('chat/',include(cha_urls)),
    path('',include(university_urls)),
    path('',include(teams_url)),
    path('', include(enactus_urls)),
]

urlpatterns+=url_doc