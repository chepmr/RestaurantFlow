from django.db import models


class Order(models.Model):
    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending'
        PREPARING = 'preparing', 'Preparing'
        READY = 'ready', 'Ready'
        SERVED = 'served', 'Served'

    table = models.ForeignKey('reservations.Table',on_delete=models.PROTECT,related_name='orders')
    dishes = models.ManyToManyField('menu.Dish',related_name='orders')
    status = models.CharField(max_length=20,choices=Status.choices,default=Status.PENDING)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Order #{self.pk} - Table {self.table.number}'