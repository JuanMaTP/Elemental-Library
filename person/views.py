from django.contrib.auth.models import User
from django_filters import rest_framework as filters
from rest_framework import generics, permissions

from general.pagination import StandardResultsSetPagination

from .filters import PersonFilter, person_view_ordering
from .permissions import IsSelfOrReadOnly
from .serializers import PersonSerializer


class PersonView(generics.ListCreateAPIView):
    """
    List all people, and register a new one (open to anyone)
    """
    permission_classes = [permissions.AllowAny]
    serializer_class = PersonSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = PersonFilter

    def get_queryset(self):
        queryset = User.objects.select_related('person').order_by('id')
        queryset = person_view_ordering(self.request.query_params, queryset)

        return queryset


class PersonDetailsView(generics.RetrieveUpdateDestroyAPIView):
    """
    Get, Update and Delete a specific Person
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsSelfOrReadOnly]
    serializer_class = PersonSerializer
    queryset = User.objects.all()

