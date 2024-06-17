from rest_framework import viewsets,permissions,generics,mixins,filters
from rest_framework.exceptions import NotFound

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from django_filters.rest_framework import DjangoFilterBackend


from apps.users.models import User
from apps.utils.utils import get_object_or_none

from .serializers import (
    Team,TeamSerializers,
    TeamProject,TeamProjectSerializer,
    TeamProjectDocuments,TeamProjectDocumentsSerializer,TeamProjectDocumentsCreateSerializer,
    TeamProjectPhotos,TeamProjectPhotosSerializer,TeamProjectPhotosCreate,
    InvitationToMembers,InvitationToMembersSerializer,
    InvitationToMembersListSerializer,
    TeamDocuments,TeamDocumentsSerializer,
    TeamMembers,TeamMembersSerializer
)

class TeamModelViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializers
    filter_backends = [DjangoFilterBackend,
                       filters.OrderingFilter,
                       filters.SearchFilter]
    ordering_fields = ['created_date','id']
    search_fields = ['name','mission', 'goals','tasks']
    filterset_fields = ['region','university']



class TeamMembersModelViewSet(viewsets.ModelViewSet):
    queryset = TeamMembers.objects.all()
    serializer_class = TeamMembersSerializer
    filter_backends = [DjangoFilterBackend,
                       filters.OrderingFilter,
                       filters.SearchFilter]
    ordering_fields = ['start_date','id']
    search_fields = ['user__first_name', 'user__last_name']
    filterset_fields = ['company','position','departament','is_current']
    


class TeamDocumentModelViewSet(viewsets.ModelViewSet):
    queryset = TeamDocuments.objects.all()
    serializer_class = TeamProjectDocumentsCreateSerializer
    filter_backends = [DjangoFilterBackend,
                       filters.OrderingFilter,
                       filters.SearchFilter]
    ordering_fields = ['id']
    search_fields = ['name','team__name']
    filterset_fields = ['team']


class TeamProjectModelViewSet(viewsets.ModelViewSet):
    queryset = TeamProject.objects.all().order_by('-id')
    serializer_class = TeamProjectSerializer
    filter_backends = [DjangoFilterBackend,
                       filters.OrderingFilter,
                       filters.SearchFilter]
    ordering_fields = ['id','start_date']
    search_fields = ['name','team__name','description','problem','decision']
    filterset_fields = ['team','region']


class TeamProjectDocumentsModelViewSet(viewsets.ModelViewSet):
    queryset = TeamProjectDocuments.objects.all()
    serializer_class = TeamProjectDocumentsSerializer
    filter_backends = [DjangoFilterBackend,
                       filters.OrderingFilter,
                       filters.SearchFilter]
    ordering_fields = ['id']
    search_fields = ['name','team_project__name']
    filterset_fields = ['team_project']


class TeamProjectPhotosModelViewSet(viewsets.ModelViewSet):
    queryset = TeamProjectPhotos.objects.all()
    serializer_class = TeamProjectPhotosCreate



class InvitationToMembersModelViewSet(viewsets.ModelViewSet):
    queryset = InvitationToMembers.objects.all()
    serializer_class = InvitationToMembersSerializer
    filter_backends = [DjangoFilterBackend,
                       filters.OrderingFilter,
                       filters.SearchFilter]
    ordering_fields = ['id']
    search_fields = ['email','first_name','last_name']
    filterset_fields = ['team','role','departament','status','invited_by']




class IinvationAUTHViewSet(mixins.RetrieveModelMixin,viewsets.GenericViewSet):
    queryset = InvitationToMembers.objects.all()
    serializer_class = InvitationToMembersListSerializer
    lookup_field = 'token'

    
    
    @swagger_auto_schema(
        operation_description="Для получение почты при регистрация пользователя",
        responses={200: InvitationToMembersListSerializer}
    )
    def get_object(self):
        queryset = self.get_queryset()
        try:
            invitation = queryset.get(token=self.kwargs['token'])
            
            if invitation.status:
                raise NotFound("Пользователь уже зарегистрирован",code=400)

            return invitation
        
        except InvitationToMembers.DoesNotExist:
            raise NotFound("Пользователь не найден")



    
