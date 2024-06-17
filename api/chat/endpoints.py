from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import api

router = DefaultRouter()
router.register('rooms', api.ChatRoomViewSet)
router.register('users', api.UserChatViewSet)
router.register('messages', api.MessageChatViewSet)
router.register('request-for-supports', api.RequestForSupportViewSet)
router.register('general-chat',api.CreateGeneralChatRoomApiView,basename="general")
router.register('add-admin-to-general-chat', api.AddAdminToGeneralChatViewSet,basename="add-admin")


urlpatterns = [
    path('messages/room/<str:uuid>/', api.MessagesByRoomChatApiView.as_view()),
    path('messages/upload-file/<str:uuid>', api.UploadFileByMessageApiView.as_view()),
    path('create-chat/', api.CreateChatRoomApiView.as_view()),
    # path('create-general-chat/', api.CreateGeneralChatRoomApiView.as_view()),
    path('request-for-supports/close-by-clinet', api.CreateChatRoomApiView.as_view()),
    # path('add-admin-to-general-chat', api.AddAdminToGeneralChatViewSet.as_view()),
    path('', include(router.urls)),
]