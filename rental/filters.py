from django_filters import rest_framework as filters

from .models import Rental


class RentalFilter(filters.FilterSet):
    book_name = filters.CharFilter(field_name="book_unit__book__name", lookup_expr='icontains')
    rental_date_gte = filters.DateTimeFilter(field_name="rental_date", lookup_expr='gte')
    rental_date_lte = filters.DateTimeFilter(field_name="rental_date", lookup_expr='lte')

    return_date_gte = filters.DateTimeFilter(field_name="return_date", lookup_expr='gte')
    return_date_lte = filters.DateTimeFilter(field_name="return_date", lookup_expr='lte')

    class Meta:
        model = Rental
        fields = ['book_name', 'book_unit__serial', 'rental_date', 'rental_date_gte', 'rental_date_lte',
                  'return_date', 'return_date_gte', 'return_date_lte']


def rentals_view_ordering(params, queryset):
    ordering = params.get('ordering', None)

    if ordering:
        if ordering == 'rental_date':
            queryset = queryset.order_by('rental_date')
        elif ordering == '-rental_date':
            queryset = queryset.order_by('-rental_date')
        elif ordering == 'return_date':
            queryset = queryset.order_by('return_date')
        elif ordering == '-return_date':
            queryset = queryset.order_by('-return_date')

    return queryset
