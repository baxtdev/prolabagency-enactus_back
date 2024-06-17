from rest_framework import permissions,filters
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.viewsets import ModelViewSet

from django_filters.rest_framework import DjangoFilterBackend

from .serializers import (
    University,UniversitySerializer,
    UniversityDocuments,UniversityDocumentsSerializer,
    UniversityDocumentsCreateSerializer
)


class UniversityModelViewSet(ModelViewSet):
    queryset = University.objects.all()
    serializer_class = UniversitySerializer
    filter_backends = [DjangoFilterBackend,
                       filters.OrderingFilter,
                       filters.SearchFilter]
    ordering_fields = ['id']
    search_fields = ['name','rectors_first_name','rectors_second_name','rectors_middle_name','info']
    filterset_fields = ['region']


class UniversityDocumentsViewSet(ModelViewSet):
    queryset = UniversityDocuments.objects.all()
    serializer_class = UniversityDocumentsCreateSerializer
    filter_backends = [DjangoFilterBackend,
                       filters.OrderingFilter,
                       filters.SearchFilter]
    ordering_fields = ['id']
    search_fields = ['university__name','name']
    filterset_fields = ['university']

