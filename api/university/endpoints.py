from django.urls import path, include
from rest_framework import routers

from . import api

router = routers.DefaultRouter()

router.register('universities',api.UniversityModelViewSet)
router.register('university-documents',api.UniversityDocumentsViewSet)

urlpatterns = [
    path('',include(router.urls))
]