from django.db import models
from django.core.validators import MinValueValidator
from project_apps.reservations.validators import validate_phone_number


class Table(models.Model):
    LOCATION_CHOICES = [
        ('indoor', 'Indoor'),
        ('terrace', 'Terrace'),
        ('garden', 'Garden'),
    ]

    number = models.PositiveSmallIntegerField(unique=True, validators=[MinValueValidator(1)])
    capacity = models.PositiveSmallIntegerField(validators=[MinValueValidator(1)])
    location = models.CharField(max_length=20, choices=LOCATION_CHOICES)
    in_service = models.BooleanField(default=True)

    def __str__(self):
        return f"Table {self.number}"


class Reservation(models.Model):
    STATUS_CHOICES = [
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]

    customer_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20, validators=[validate_phone_number])
    date = models.DateField()
    time = models.TimeField()
    guests_count = models.PositiveSmallIntegerField(validators=[MinValueValidator(1)])
    tables = models.ManyToManyField(Table, related_name='reservations')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='confirmed')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer_name} - {self.date} {self.time}"