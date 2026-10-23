import re

from django.core.exceptions import ValidationError


def validate_phone_number(value):
    if not re.fullmatch(r'\+?[0-9]{8,15}', value):
        raise ValidationError(
            'Enter a valid phone number (8-15 digits).'
        )