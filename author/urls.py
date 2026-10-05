from django.urls import path

from .views import AuthorDetailsView, AuthorView

urlpatterns = [
    path('', AuthorView.as_view()),
    path('<int:pk>/', AuthorDetailsView.as_view()),
]
