from django.urls import path
from mesero.presentation.views.owner_view import OwnerCreateView

urlpatterns = [
    path('owners/', OwnerCreateView.as_view(), name='create-owner'),
]
