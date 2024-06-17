from rest_framework import serializers 


from apps.utils.fields import Base64FileField
from drf_extra_fields.fields import HybridImageField
from drf_writable_nested import WritableNestedModelSerializer

from apps.enactus.models import Advertisement,Project,News,\
                                NewsCategory,NewsPhoto,Event
                                
class AdvertisementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Advertisement
        fields = '__all__'



class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'



class NewsCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsCategory
        fields = '__all__'



class NewsPhotoSerializer(serializers.ModelSerializer):
    image = HybridImageField()
    image_data = serializers.ImageField(source='image',read_only=True)
    class Meta:
        model = NewsPhoto
        fields = '__all__'



class NewsSerializer(WritableNestedModelSerializer):
    photos = NewsPhotoSerializer(many=True)
    class Meta:
        model = News
        fields = '__all__'



class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'