from django.urls import include, path

from rest_framework import routers

from . import api

router = routers.DefaultRouter()

router.register('teams',api.TeamModelViewSet)
router.register('teams-documents',api.TeamDocumentModelViewSet)
router.register('teams-projects',api.TeamProjectModelViewSet)
router.register('teams-projects-documents',api.TeamProjectDocumentsModelViewSet)
router.register('teams-projects-photos',api.TeamProjectPhotosModelViewSet)
router.register('invitation-to-members',api.InvitationToMembersModelViewSet,'invitations')
router.register('accounts/get-email/invited/users',api.IinvationAUTHViewSet,'invitations-emails')
router.register('team-members',api.TeamMembersModelViewSet)

urlpatterns = [
    path('',include(router.urls))
]