from django.urls import include, path

from rest_framework import routers

from . import api

router = routers.DefaultRouter()
router.register('projects', api.ProjectModelViewSet)
router.register('advertisements', api.AdvertisementModelViewSet)
router.register('news', api.NewsModelViewSet)
router.register('news-categories', api.NewsCategoryModelViewSet)
router.register('news-photos', api.NewsPhotoModelViewSet)
router.register('events', api.EventModelViewSet)


urlpatterns = [
    path('',include(router.urls))
]