from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import render
from .serializers import ActivitySerializer, FoodLogSerializer, WeightLogSerializer
from .models import Activity, FoodLog, WeightLog
from django.db.models import Sum
from rest_framework import generics, permissions, filters
from rest_framework.views import APIView
from rest_framework.response import Response
# Create your views here.

class ActivityListCreateView(generics.ListCreateAPIView):
    queryset = Activity.objects.all()

    serializer_class = ActivitySerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = {
        'activity_type': ['exact'],
        'date': ['exact', 'gte', 'lte'], # gte = greater than or equal, lte = less than or equal
    }
    ordering_fields = ['date', 'duration_minutes', 'calories_burned']
    ordering = ['-date']

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
    queryset = FoodLog.objects.all()

    serializer_class = FoodLogSerializer
    permission_classes = [permissions.IsAuthenticated]

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['meal_type', 'food_item', 'date']

    def get_queryset(self):
        return FoodLog.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class WeightLogListCreateView(generics.ListCreateAPIView):
    
    queryset = WeightLog.objects.all()
    serializer_class = WeightLogSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['date']

    def get_queryset(self):
        return WeightLog.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ActivitySummaryView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user_activities = Activity.objects.filter(user=request.user)
        user_food = FoodLog.objects.filter(user=request.user)

        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')

        if start_date and end_date:
            user_activities = user_activities.filter(date__range=[start_date, end_date])
            user_food = user_food.filter(date__range=[start_date, end_date])

        activity_summary = user_activities.aggregate(
            total_duration=Sum('duration_minutes'),
            total_distance=Sum('distance_km'),
            total_calories_burned=Sum('calories_burned')
        )

        food_summary = user_food.aggregate(
            total_calories_ingested=Sum('calories_ingested'),
            total_protein=Sum('protein'),
            total_carbs=Sum('carbs'),
            total_fats=Sum('fats')
        )
        
        return Response({
            "activity": activity_summary,
            "nutrition": food_summary
        })