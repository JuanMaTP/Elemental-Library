from django.urls import path

from .views import RentalBorrowView, RentalDetailsView, RentalReturnView, RentalView

urlpatterns = [
    path('', RentalView.as_view()),
    path('borrow/', RentalBorrowView.as_view()),
    path('return/<int:pk>/', RentalReturnView.as_view()),
    path('<int:pk>/', RentalDetailsView.as_view()),
]
