from rest_framework import serializers
from .models import Activity, FoodLog, WeightLog

class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = ['id', 'activity_type', 'duration_minutes', 'distance_km', 'calories_burned', 'date']
        
class FoodLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodLog
        fields = ['id', 'meal_type', 'food_item', 'calories_ingested', 'protein', 'carbs', 'fats','date']

class WeightLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeightLog
        fields = ['id', 'weight_kg', 'date']