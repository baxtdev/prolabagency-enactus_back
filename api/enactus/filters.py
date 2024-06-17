import django_filters

from .serializers import News


class NewsFilterSet(django_filters.FilterSet):
    search = django_filters.CharFilter(field_name=['title','description','short_description'],lookup_expr='icontains',label='search results')
    class Meta:
        model = News
        fields = ('search',)
