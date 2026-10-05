from django.urls import path

from .views import PersonDetailsView, PersonView

urlpatterns = [
    path('', PersonView.as_view(), name='people-list'),
    path('<int:pk>/', PersonDetailsView.as_view(), name='person-details'),
]
