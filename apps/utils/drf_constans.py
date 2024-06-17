from rest_framework.permissions import IsAuthenticated, AllowAny

from api.permissions import IsSuperAdmin

USE_PAGINATION = 'use_pagination'
DEFAULT_PERMISSION = {
        'create': (IsAuthenticated, IsSuperAdmin),
        'list': (AllowAny,),
        'update': (IsAuthenticated, IsSuperAdmin),
        'retrieve': (AllowAny,),
        'destroy': (IsAuthenticated, IsSuperAdmin),
    }