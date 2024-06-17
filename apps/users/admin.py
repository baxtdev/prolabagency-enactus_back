from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.utils.translation import gettext_lazy as _


from .models import User,ResetPasword,UserActivities

from apps.teams.models import InvitationToMembers

class InvitationToMembersInline(admin.TabularInline):
    model = InvitationToMembers
    extra = 0  

    def get_queryset(self, request):
        user_email = request.user.email if request.user.is_authenticated else None
        
        queryset = super().get_queryset(request)
        if user_email:
            queryset = queryset.filter(email=user_email)
        else:
            queryset = queryset.none()
        return queryset


# Register your models here.
class UserActivitiesInline(admin.TabularInline):
    model = UserActivities
    extra = 0

    

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    inlines = [UserActivitiesInline,]
    list_display = ('email', 'get_full_name', 'phone', 'last_activity','id')
    readonly_fields = ('last_activity','last_login','date_joined',)
    
    fieldsets = (
        (None, {'fields': (
            'email',
            'phone',
            'password',
            'role'
        )}),
        (_('Personal info'), {'fields': (
            'image',
            'first_name',
            'last_name',
            'middle_name',
            'gender',
        )}),
        (_('Permissions'), {'fields': (
            'is_active',
            'is_staff',
            'is_superuser',
            'groups',
            'user_permissions',
        )}),
        (_('Important dates'), {'fields': (
            'date_joined',
            'last_login',
            'last_activity',
        )}),
        (_('Social Network'), {'fields': (
            'instagram_url',
            'telegram_url',
            'tik_tok_url',
            'twitter_url',
            'youtube_url',
            'facebook_url',

        )}),
        
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email',
                'phone',
                'password1',
                'password2',
            ),
        }),
    )

    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)


@admin.register(ResetPasword)
class ResetPasswordAdmin(admin.ModelAdmin):
    pass

@admin.register(UserActivities)
class UserActivitiesAdmin(admin.ModelAdmin):
    pass