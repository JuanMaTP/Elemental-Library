from django.contrib.auth.models import User
from django.db.models.functions import Lower
from django_filters import rest_framework as filters


class PersonFilter(filters.FilterSet):
    name = filters.CharFilter(field_name="username", lookup_expr='icontains')
    birth_date_gte = filters.DateFilter(field_name="person__birth_date", lookup_expr='gte')
    birth_date_lte = filters.DateFilter(field_name="person__birth_date", lookup_expr='lte')

    class Meta:
        model = User
        fields = ['username', 'person__gender', 'person__birth_date', 'birth_date_gte', 'birth_date_lte']


def person_view_ordering(params, queryset):
    ordering = params.get('ordering', None)

    if ordering:
        if ordering == 'name':
            queryset = queryset.order_by(Lower('username'))
        elif ordering == '-name':
            queryset = queryset.order_by(Lower('username').desc())
        elif ordering == 'birth_date':
            queryset = queryset.order_by('person__birth_date')
        elif ordering == '-birth_date':
            queryset = queryset.order_by('-person__birth_date')

    return queryset
