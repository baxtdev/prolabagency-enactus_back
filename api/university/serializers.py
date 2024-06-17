from rest_framework import serializers 
from drf_extra_fields.relations import PresentablePrimaryKeyRelatedField
from drf_writable_nested import WritableNestedModelSerializer
from apps.utils.fields import Base64FileField

from apps.university.models import University,UniversityDocuments



class UniversityDocumentsSerializer(serializers.ModelSerializer):
    document_file = Base64FileField(write_only=True)
    document_file_data = serializers.ImageField(source='document_file',read_only=True)

    class Meta:
        model = UniversityDocuments
        fields = '__all__'
        read_only_fields = ['university',]



class UniversityDocumentsCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UniversityDocuments
        fields = '__all__'



class UniversitySerializer(WritableNestedModelSerializer):
    documents = UniversityDocumentsSerializer(many=True,)
    image = Base64FileField(write_only=True)
    image_data = serializers.ImageField(source='image',read_only=True)

    class Meta:
        model = University
        fields = '__all__'



