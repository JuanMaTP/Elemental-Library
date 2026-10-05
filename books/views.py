from django.utils.crypto import get_random_string
from django_filters import rest_framework as filters
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import generics

from general.pagination import LargeResultsSetPagination, StandardResultsSetPagination
from general.permissions import IsAdminOrReadOnly

from .filters import BookFilter, BookUnitFilter, book_units_view_ordering, books_view_ordering
from .models import Book, BookUnit
from .serializers import BookAddUnitSerializer, BookSerializer, BookUnitSerializer


class BookView(generics.ListCreateAPIView):
    """
    List and Create Books
    """
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = BookSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = BookFilter

    def get_queryset(self):
        queryset = Book.objects.order_by('id')

        queryset = books_view_ordering(self.request.query_params, queryset)

        return queryset


@extend_schema_view(post=extend_schema(operation_id='api_books_units_create', summary='Add a BookUnit to this Book'))
class BookDetailView(generics.RetrieveUpdateDestroyAPIView, generics.CreateAPIView):
    """
    GET, PUT, PATCH and DELETE a Book
    POST a BookUnit with an input serial number or an internally generated one
    """
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = BookAddUnitSerializer
    queryset = Book.objects.all()

    def perform_create(self, serializer):
        # A POST here adds a new BookUnit to this Book instead of creating a Book.
        # The response then shows the Book with its units, including the new one.
        book = self.get_object()
        serial = serializer.validated_data.get('serial') or get_random_string(length=16)
        BookUnit.objects.create(book=book, serial=serial)
        serializer.instance = book


class BookUnitView(generics.ListAPIView):
    """
    Lists all of the BookUnits
    """

    serializer_class = BookUnitSerializer
    pagination_class = LargeResultsSetPagination
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = BookUnitFilter

    def get_queryset(self):
        queryset = BookUnit.objects.select_related('book').order_by('id')
        queryset = book_units_view_ordering(self.request.query_params, queryset)

        return queryset


@extend_schema_view(
    get=extend_schema(operation_id='api_books_units_retrieve'),
    put=extend_schema(operation_id='api_books_units_update'),
    patch=extend_schema(operation_id='api_books_units_partial_update'),
    delete=extend_schema(operation_id='api_books_units_destroy'),
)
class BookUnitDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Returns a BookUnit (id) that belongs to a Book (book_id)
    """
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = BookUnitSerializer

    # Narrows down the BookUnits that belong to the specified Book
    # And then gets the specific BookUnit by the pk
    def get_queryset(self):
        pk = self.kwargs.get('pk')
        book_id = self.kwargs.get('book_id')
        return BookUnit.objects.filter(pk=pk, book__pk=book_id)
