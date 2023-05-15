from django.db import models
from django.contrib.auth.models import User

class CalorieEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    food_item = models.CharField(max_length=255)
    quantity = models.DecimalField(max_digits=5, decimal_places=2)
    calories = models.DecimalField(max_digits=6, decimal_places=2)
    date = models.DateField(auto_now_add=True)
