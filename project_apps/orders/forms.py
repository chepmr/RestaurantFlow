from django import forms

from project_apps.orders.models import Order
from project_apps.menu.models import Dish
from project_apps.reservations.models import Table


class OrderForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = ['table', 'dishes', 'notes']

        labels = {
            'table': 'Table',
            'dishes': 'Dishes',
            'notes': 'Additional Notes',
        }

        widgets = {
            'table': forms.Select(attrs={
                'class': 'form-select',
            }),
            'dishes': forms.CheckboxSelectMultiple(),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Any instructions for your order.?',
                'rows': 3,
            }),
        }

        help_texts = {
            'table': 'Select the table for your order.',
            'dishes': 'Select at least one dish.',
            'notes': 'Optional instructions for your order.',
        }

        error_messages = {
            'table': {
                'required': 'Please select a table.',
                'invalid_choice': 'Please select a valid table.',
            },
            'dishes': {
                'required': 'Please select at least one dish.',
                'invalid_choice': 'Please select valid dishes.',
            },
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['table'].queryset = Table.objects.filter(
            in_service=True
        ).order_by('number')

        self.fields['dishes'].queryset = Dish.objects.filter(
            is_available=True
        ).order_by('category', 'name')

        self.fields['dishes'].label_from_instance = (
            lambda dish: f'{dish.name} - {dish.price:.2f} €'
        )


class OrderUpdateForm(OrderForm):
    class Meta(OrderForm.Meta):
        fields = ['table', 'dishes', 'status', 'notes']

        labels = {
            **OrderForm.Meta.labels,
            'status': 'Order Status',
        }

        widgets = {
            **OrderForm.Meta.widgets,
            'status': forms.Select(attrs={
                'class': 'form-select',
            }),
        }

        help_texts = {
            **OrderForm.Meta.help_texts,
            'status': 'Select the current status of the order.',
        }

        error_messages = {
            **OrderForm.Meta.error_messages,
            'status': {
                'invalid_choice': 'Please select a valid order status.',
            },
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance.pk:
            self.fields['table'].queryset = Table.objects.filter(
                pk=self.instance.table_id
            )

        self.fields['table'].disabled = True