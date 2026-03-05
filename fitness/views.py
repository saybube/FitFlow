from django.shortcuts import render
from .serializers import ActivitySerializer, FoodLogSerializer, WeightLogSerializer
from .models import Activity, FoodLog, WeightLog
from django.db.models import Sum
from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
# Create your views here.

class ActivityListCreateView(generics.ListCreateAPIView):
    serializer_class = ActivitySerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        return Activity.objects.filter(user=self.request.user)
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ActivityDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ActivitySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Activity.objects.filter(user=self.request.user)
    
class FoodLogListCreateView(generics.ListCreateAPIView):
    serializer_class = FoodLogSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return FoodLog.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class WeightLogListCreateView(generics.ListCreateAPIView):
    serializer_class = WeightLogSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return WeightLog.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ActivitySummaryView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user_activities = Activity.objects.filter(user=request.user)
        summary = user_activities.aggregate(
            total_duration=Sum('duration_minutes'),
            total_distance=Sum('distance_km'),
            total_calories=Sum('calories_burned')
        )
        
        return Response(summary)