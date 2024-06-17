from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.mixins import ListModelMixin
from rest_framework import permissions,filters,status
from django_filters.rest_framework import DjangoFilterBackend



from .serializers import (
    Project,ProjectSerializer,
    Advertisement,AdvertisementSerializer,
    News,NewsSerializer,
    NewsCategory,NewsCategorySerializer,
    NewsPhoto,NewsPhotoSerializer,
    Event,EventSerializer,
)
from .filters import NewsFilterSet

class ProjectModelViewSet(ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer



class NewsModelViewSet(ModelViewSet):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    filter_backends = [DjangoFilterBackend,
                       filters.OrderingFilter,
                       filters.SearchFilter]
    ordering_fields = ['created_at']
    search_fields = ['title', 'description', 'short_description', 'category__name']
    filterset_fields = ['category']



class NewsCategoryModelViewSet(ModelViewSet):
    queryset = NewsCategory.objects.all()
    serializer_class = NewsCategorySerializer
    filter_backends = [DjangoFilterBackend,
                       filters.SearchFilter]
    ordering_fields = ['id']
    search_fields = ['name']



class NewsPhotoModelViewSet(ModelViewSet):
    queryset = NewsPhoto.objects.all()
    serializer_class = NewsPhotoSerializer



class AdvertisementModelViewSet(ModelViewSet):
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    filter_backends = [DjangoFilterBackend,
                       filters.OrderingFilter,
                       filters.SearchFilter]
    ordering_fields = ['created_at']
    search_fields = ['theme', 'description']





class EventModelViewSet(ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    filter_backends = [DjangoFilterBackend,
                       filters.OrderingFilter,
                       filters.SearchFilter]
    ordering_fields = ['start_date','id']
    search_fields = ['name', 'short_description','description']
    filterset_fields = ['region']
    



