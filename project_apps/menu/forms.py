from django import forms

from project_apps.menu.models import Dish


class DishForm(forms.ModelForm):
    class Meta:
        model = Dish
        fields = '__all__'

        labels = {
            'name': 'Dish Name',
            'category': 'Category',
            'description': 'Description',
            'price': 'Price',
            'is_available': 'Available',
        }

        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Enter dish name',
            }),
            'category': forms.Select(),
            'description': forms.Textarea(attrs={
                'placeholder': 'Enter dish description',
                'rows': 4,
            }),
            'price': forms.NumberInput(attrs={
                'placeholder': 'Enter price',
                'min': '0.5',
                'step': '1',
            }),
            'is_available': forms.CheckboxInput(),
        }

        help_texts = {
            'name': 'Enter the name for your preferred dish.',
            'category': 'Select dish category.',
            'description': 'Description of the dish.',
            'price': 'Enter a price.',
            'is_available': 'Check if the dish is available for ordering.',
        }

        error_messages = {
            'name': {
                'required': 'Dish name is required.',
                'unique': 'A dish with this name already exists.',
                'max_length': 'Dish name is too long.',
            },
            'category': {
                'required': 'Please select a category.',
                'invalid_choice': 'Please select a valid category.',
            },
            'price': {
                'required': 'Dish price is required.',
                'invalid': 'Please enter a valid price.',
                'min_value': 'Price must be at least 0.50.',
                'max_digits': 'The price contains too many digits.',
            },
        }