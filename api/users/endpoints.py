from django.urls import path, include
from rest_framework import routers

from . import api

router = routers.DefaultRouter()
router.register('regions',api.RegionReadOnlyModelViewSet)
router.register('users',api.UserModeliewSet)

urlpatterns = [
    path('', include(router.urls))
]