from django.contrib import admin
from .models import CalorieEntry

# Register your models here.
 
@admin.register(CalorieEntry)

class CalorieEntryAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'food_item', 'quantity', 'calories', 'date']