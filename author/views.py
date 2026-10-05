from django_filters import rest_framework as filters
from rest_framework import generics

from general.pagination import SmallResultsSetPagination
from general.permissions import IsAdminOrReadOnly

from .filters import AuthorFilter, authors_view_ordering
from .models import Author
from .serializers import AuthorSerializer


class AuthorView(generics.ListCreateAPIView):
    """
    Lists and creates a new Author
    """
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = AuthorSerializer
    pagination_class = SmallResultsSetPagination
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = AuthorFilter

    def get_queryset(self):
        queryset = Author.objects.order_by('id')
        queryset = authors_view_ordering(self.request.query_params, queryset)

        return queryset


class AuthorDetailsView(generics.RetrieveUpdateDestroyAPIView):
    """
    Get, Update and Delete a specific Rental
    """
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = AuthorSerializer
    queryset = Author.objects.all()
