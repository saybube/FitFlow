from django.db import models
from django.conf import settings

# Create your models here.
# 1. Fitness Activities Model
class Activity(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='activities')
    activity_type = models.CharField(max_length=50) # e.g., Running, Cycling
    duration_minutes = models.PositiveIntegerField()
    distance_km = models.FloatField(null=True, blank=True)
    calories_burned = models.FloatField()
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.activity_type} - {self.user.username}"
    
# 2. Food Log Model
class FoodLog(models.Model):
    MEAL_CHOICES = [
        ('Breakfast', 'Breakfast'),
        ('Lunch', 'Lunch'),
        ('Dinner', 'Dinner'),
        ('Snack', 'Snack'),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='foods')
    meal_type = models.CharField(max_length=20, choices=MEAL_CHOICES)
    food_item = models.CharField(max_length=100)
    calories_ingested = models.FloatField()
    protein = models.FloatField(default=0.0)
    carbs = models.FloatField(default=0.0)
    fats = models.FloatField(default=0.0)
    date = models.DateField()

    def __str__(self):
        return f"{self.food_item} - {self.user.username}"
    
# 3. Weight Measurement Model
class WeightLog(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='weights')
    weight_kg = models.FloatField()
    date = models.DateField()

    def __str__(self):
        return f"{self.user.username} - {self.weight_kg}kg"