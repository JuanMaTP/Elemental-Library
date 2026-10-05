from django.db.models.functions import Lower
from django_filters import rest_framework as filters

from author.models import Author


class AuthorFilter(filters.FilterSet):
    name = filters.CharFilter(field_name="name", lookup_expr='icontains')
    birth_date_gte = filters.DateFilter(field_name="birth_date", lookup_expr='gte')
    birth_date_lte = filters.DateFilter(field_name="birth_date", lookup_expr='lte')

    class Meta:
        model = Author
        fields = ['name', 'gender', 'birth_date', 'birth_date_gte', 'birth_date_lte']


def authors_view_ordering(params, queryset):
    ordering = params.get('ordering', None)

    if ordering:
        if ordering == 'name':
            queryset = queryset.order_by(Lower('name'))
        elif ordering == '-name':
            queryset = queryset.order_by(Lower('name').desc())
        elif ordering == 'birth_date':
            queryset = queryset.order_by('birth_date')
        elif ordering == '-birth_date':
            queryset = queryset.order_by('-birth_date')

    return queryset
