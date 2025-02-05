from django.urls import path
from mesero.presentation.views.owner_view import OwnerCreateView
from mesero.presentation.views.plan_view import PlanCreateView, PlanUpdateView, PlanDeleteView

urlpatterns = [
    path('owners/create', OwnerCreateView.as_view(), name='create-owner'),
    path('plans/create', PlanCreateView.as_view(), name='create_plan'),
    path('plans/update/<int:pk>/', PlanUpdateView.as_view(), name='update_plan'),
    path('plans/delete/<int:pk>/', PlanDeleteView.as_view(), name='delete_plan'),
]
