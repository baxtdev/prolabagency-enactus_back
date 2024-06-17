from typing import Any
from django.contrib import admin

from .models import Team,TeamProject,TeamProjectDocuments,TeamProjectPhotos,\
    InvitationToMembers,TeamDocuments,TeamMembers


class TeamProjectDocumentsInline(admin.TabularInline):
    model = TeamProjectDocuments
    extra = 0

class TeamProjectPhotosInline(admin.TabularInline):
    model = TeamProjectPhotos
    extra = 0
    readonly_fields = ('image_absolute_url',)    

class TeamIProjectnline(admin.TabularInline):
    model = TeamProject
    extra = 0
    readonly_fields = ('name','start_date','end_date','is_current',)
    fields = ('name','start_date','end_date','is_current',)
    can_delete = False
    show_change_link = True

class TeamDocumentsInline(admin.TabularInline):
    model = TeamDocuments
    extra = 0


# Register your models here.
@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    inlines = [TeamIProjectnline,TeamDocumentsInline]


@admin.register(TeamMembers)
class TeamMembersAdmin(admin.ModelAdmin):
    pass

@admin.register(TeamProject)
class TeamProjectAdmin(admin.ModelAdmin):
    inlines = [TeamProjectDocumentsInline, TeamProjectPhotosInline]


@admin.register(InvitationToMembers)
class InvationToMembersAdmin(admin.ModelAdmin):
    readonly_fields = ('invited_by','token')

    def save_model(self, request: Any, obj: Any, form: Any, change: Any) -> None:
        obj.invited_by = request.user
        return super().save_model(request, obj, form, change)


