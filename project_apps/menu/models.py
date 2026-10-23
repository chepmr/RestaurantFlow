from decimal import Decimal

from django.db import models
from django.core.validators import MinValueValidator
from project_apps.menu.validators import validate_dish_name


class Dish(models.Model):
    DISH_CHOICES = [
        ('starter', 'Starter'),
        ('drink', 'Drink'),
        ('main_dish', 'Main Dish'),
        ('dessert', 'Dessert'),
    ]

    name = models.CharField(max_length=100, unique=True,validators=[validate_dish_name])
    category = models.CharField(max_length=20, choices=DISH_CHOICES)
    description = models.TextField(blank=True)
    price = models.DecimalField(decimal_places=2,max_digits=10,validators=[MinValueValidator(Decimal('0.50'))])
    is_available = models.BooleanField(default=True)

    class Meta:
        ordering = ['category', 'name']

    def __str__(self):
        return self.name
