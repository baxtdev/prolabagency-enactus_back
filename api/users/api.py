from django.utils.timezone import datetime
from rest_registration.utils.responses import get_ok_response
from rest_registration.api.serializers import DefaultUserProfileSerializer

from rest_framework.exceptions import NotFound
from rest_framework.authtoken.models import Token
from rest_framework import permissions,viewsets,mixins,filters
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView

from django_filters.rest_framework import DjangoFilterBackend

from ..mixins import SuperReadOnlyAndDestroyModelViewSet

from api.users.serializers import (
    GoogleAuthSerializer, 
    RegisterUserSerializer,
    ResetPasswordSerializer,ResetPasword, 
    UserProfileSerializer,User,
    Region,RegionSerializers,
    UserSerilizer
    )
from apps.users.tasks import send_email

class RegisterAPIView(GenericAPIView):
    serializer_class = RegisterUserSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = Token.objects.get_or_create(user=user)[0]
        user_serializer = UserProfileSerializer(instance=user, context={'request': request})
        return Response({
            **user_serializer.data,
            'token': token.key,
        })



class GoogleAuthAPIView(GenericAPIView):
    serializer_class =  GoogleAuthSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = Token.objects.get_or_create(user=user)[0]
        user_serializer = DefaultUserProfileSerializer(instance=user, context={'request': request})
        return Response({
            **user_serializer.data,
            'token': token.key,
        })
    
    
class GetResetPasswordCodeAPI(GenericAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    lookup_field = 'email'

    def get_object(self):
        queryset = self.get_queryset()
        try:
            user = queryset.get(email=self.kwargs['email'])
            return user
        
        except User.DoesNotExist:
            raise NotFound("Пользователь не найден")

    def get(self, request, *args, **kwargs):
        user = self.get_object()
        response = ResetPasword.objects.create(
                user=user,
                is_active=True
            )
            
        data = response.code
        res = send_email.apply_async(args=[data, user.email], countdown=10)
        if res:
            return get_ok_response(('вам отправлен код'))
        else:
            return Response({"detail": "Не удалось отправить код"}, status=500)
        

class ChekingCodeAPI(GenericAPIView):
    queryset = ResetPasword.objects.all()
    permission_classes = [permissions.AllowAny]
    lookup_field = 'code'

    def get(self, request, *args, **kwargs):
        data=self.get_object()
        if data.is_active:
            return get_ok_response("этот код активен")
        else:
            return Response({"detail":"этот код не активен"},404)



class ResetPasswordAPIView(GenericAPIView):
    queryset = ResetPasword.objects.filter(is_active=True)
    permission_classes = (permissions.AllowAny,)
    lookup_field = 'code'
    serializer_class = ResetPasswordSerializer   

    def get_object(self):
        queryset = self.get_queryset()
        try:
            user = queryset.get(code=self.kwargs['code'])
            return user
        
        except ResetPasword.DoesNotExist:
            raise NotFound("Код не подерживается")

    def post(self, request, *args, **kwargs):
        data_t=datetime.today()
        reset_object = self.get_object()
        if reset_object:
            if reset_object.data==data_t.date():    
                serializer = self.serializer_class(data=request.data)
                serializer.is_valid(raise_exception=True)
                password=serializer.validated_data.get('password')
                reset_object.user.set_password(password)
                reset_object.user.save()
                reset_object.is_active=False
                reset_object.save()
                reset_object.delete()
                return get_ok_response(("your password is changed"))  
            else:
                return Response({"detail":"this code is inactive"},404)
        else:
            return Response({"detail":"not defound"},400)    



class UserModeliewSet(SuperReadOnlyAndDestroyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerilizer
    permission_classes = [permissions.IsAdminUser]
    filter_backends = [DjangoFilterBackend,
                       filters.OrderingFilter,
                       filters.SearchFilter]
    search_fields = ['phone','middle_name','email','first_name','last_name']
    ordering_fields = ['id','last_activity','date_joined']
    filterset_fields = ['is_active','is_staff','is_superuser','gender','role','is_notifications']


    def get_queryset(self):
        queryset=super().get_queryset()
        return queryset.exclude(self.request.user)


class RegionReadOnlyModelViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Region.objects.all()
    serializer_class = RegionSerializers
    filter_backends = [filters.SearchFilter,
                       filters.OrderingFilter]
    ordering_fields = ['id']
    search_fields = ['name']
