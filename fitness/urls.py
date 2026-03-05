from django.urls import path
from .views import ActivityListCreateView, ActivityDetailView, FoodLogListCreateView, WeightLogListCreateView

urlpatterns = [
    path('activities/', ActivityListCreateView.as_view(), name='activity-list'),
    path('activities/<int:pk>/', ActivityDetailView.as_view(), name='activity-detail'),
    path('food/', FoodLogListCreateView.as_view(), name='food-list'),
    path('weight/', WeightLogListCreateView.as_view(), name='weight-list'),
]