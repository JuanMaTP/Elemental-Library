from django_filters import rest_framework as filters
from rest_framework import generics, permissions

from general.pagination import LargeResultsSetPagination
from general.permissions import IsAdminOrReadOnly

from .filters import RentalFilter, rentals_view_ordering
from .models import Rental
from .permissions import IsRenterOrAdmin
from .serializers import RentalReturnSerializer, RentalSerializer


class RentalView(generics.ListAPIView):
    """
    Lists all of the created Rentals
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = RentalSerializer
    pagination_class = LargeResultsSetPagination
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = RentalFilter

    def get_queryset(self):
        queryset = Rental.objects.select_related('person__user', 'book_unit__book').order_by('id')
        queryset = rentals_view_ordering(self.request.query_params, queryset)

        return queryset


class RentalBorrowView(generics.CreateAPIView):
    """
    Creates a new Rental: takes the BookUnit to borrow and assigns the logged-in
    person and the current date
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = RentalSerializer
    queryset = Rental.objects.all()


class RentalReturnView(generics.UpdateAPIView):
    """
    'Returns' a BookUnit: sets the rental's return_date to now and makes the unit available again
    """
    permission_classes = [permissions.IsAuthenticated, IsRenterOrAdmin]
    serializer_class = RentalReturnSerializer
    queryset = Rental.objects.select_related('person')


class RentalDetailsView(generics.RetrieveUpdateDestroyAPIView):
    """
    Get, Update and Delete a specific Rental
    """
    permission_classes = [permissions.IsAuthenticated, IsAdminOrReadOnly]
    serializer_class = RentalSerializer
    queryset = Rental.objects.all()
