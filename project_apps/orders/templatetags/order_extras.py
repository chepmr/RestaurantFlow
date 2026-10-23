from django import template

register = template.Library()


@register.filter
def order_total(order):
    return sum(dish.price for dish in order.dishes.all())