import re

from django.core.exceptions import ValidationError


def validate_dish_name(value):
    if not re.fullmatch(r'[^\W_]+(?:[ -][^\W_]+)*', value):
        raise ValidationError('Dish name can contain only letters, numbers, spaces and hyphens.')

    if not any(char.isalpha() for char in value):
        raise ValidationError('Please enter a valid dish name.')