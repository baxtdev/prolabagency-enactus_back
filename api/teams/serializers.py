from rest_framework import serializers

from apps.utils.fields import Base64FileField
from drf_extra_fields.fields import HybridImageField

from drf_extra_fields.relations import PresentablePrimaryKeyRelatedField
from drf_writable_nested import WritableNestedModelSerializer

from apps.teams.models import Team,TeamProject,TeamProjectDocuments,\
        TeamProjectPhotos,InvitationToMembers,TeamDocuments,TeamMembers
              
                

class TeamProjectDocumentsSerializer(serializers.ModelSerializer):
    document_file = Base64FileField(write_only=True)
    document_data = serializers.FileField(
        source='document_file',
        read_only=True,
    )

    class Meta:
        model = TeamProjectDocuments
        fields = '__all__'
        read_only_fields = ['team_project',]


class TeamProjectDocumentsCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamProjectDocuments
        fields = '__all__'


class TeamProjectPhotosSerializer(serializers.ModelSerializer):
    image = HybridImageField(write_only=True)
    image_data = serializers.ImageField(source='image',read_only=True)

    class Meta:
        model = TeamProjectPhotos
        fields = '__all__'
        read_only_fields = ['team_project',]


class TeamProjectPhotosCreate(serializers.ModelSerializer):
    class Meta:
        model = TeamProjectPhotos
        fields = '__all__'


class TeamProjectSerializer(WritableNestedModelSerializer):
    documents = TeamProjectDocumentsSerializer(many=True,)
    photos = TeamProjectPhotosSerializer(many=True,)
    class Meta:
        model = TeamProject
        fields = '__all__'


class TeamDocumentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamDocuments
        fields = '__all__'



class TeamMembersSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamMembers
        fields = '__all__'
        


class TeamSerializers(serializers.ModelSerializer):
    projects =TeamProjectSerializer(many=True,read_only=True)
    class Meta:
        model = Team
        fields = '__all__'



class InvitationToMembersSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvitationToMembers
        fields = '__all__'



class InvitationToMembersListSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvitationToMembers
        fields = ('email',)

        


