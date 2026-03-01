from django.contrib import admin
from .models import Activity, FoodLog, WeightLog

# Register your models here.
admin.site.register(Activity)
admin.site.register(FoodLog)
admin.site.register(WeightLog)