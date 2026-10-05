from django.urls import path

from .views import BookDetailView, BookUnitDetailView, BookUnitView, BookView

urlpatterns = [
    path('', BookView.as_view()),
    path('units/', BookUnitView.as_view()),
    path('<int:pk>/', BookDetailView.as_view()),
    path('<int:book_id>/<int:pk>/', BookUnitDetailView.as_view()),
]
