from django import forms
from project_apps.reservations.models import Table, Reservation
from datetime import datetime, timedelta
from django.utils import timezone


class TableForm(forms.ModelForm):
    class Meta:
        model = Table
        fields =  '__all__'

        labels = {
            'number': 'Table Number',
            'capacity': 'Capacity',
            'location': 'Location',
            'in_service': 'Available',
        }

        widgets = {
            'number': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter table number', 'min': 1}),
            'capacity': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter capacity', 'min': 1}),
            'location': forms.Select(attrs={'class': 'form-select'}),
            'in_service': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

        help_texts = {
            'number': 'Enter an available table number.',
            'capacity': 'Enter the total number of guests.',
            'location': 'Select where the table is located.',
            'in_service': 'Uncheck if the table is out of service.',
        }

        error_messages = {
            'number': {
                'required': 'Table number is required.',
                'unique': 'A table with this number already exists.',
                'invalid': 'Enter a valid table number.',
            },
            'capacity': {
                'required': 'Table capacity is required.',
                'invalid': 'Enter a valid capacity.',
                'min_value': 'There should be at least 1 guest.',
            },
            'location': {
                'required': 'Please select a location.',
                'invalid_choice': 'Select a valid location.',
            },
        }




class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['customer_name', 'phone_number', 'date', 'time', 'guests_count', 'tables']

        labels = {
            'customer_name': 'Full Name',
            'phone_number': 'Phone Number',
            'date': 'Reservation Date',
            'time': 'Reservation Time',
            'guests_count': 'Number of Guests',
            'tables': 'Select Tables',
        }

        widgets = {
            'customer_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your full name'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+359888123456'}),
            'date': forms.DateInput(format='%Y-%m-%d', attrs={'class': 'form-control', 'type': 'date'}),
            'time': forms.TimeInput(format='%H:%M', attrs={'class': 'form-control', 'type': 'time'}),
            'guests_count': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Number of guests', 'min': 1}),
            'tables': forms.CheckboxSelectMultiple(),
        }

        help_texts = {
            'customer_name': 'Enter the name for the reservation.',
            'phone_number': 'Enter a valid phone number.',
            'date': 'Select the preferred date of your reservation.',
            'time': 'Select the preferred starting time. Reservations last 2 hours.',
            'guests_count': 'Enter the total number of guests.',
            'tables': 'Select one or more tables with enough capacity for your guests.',
        }

        error_messages = {
            'customer_name': {
                'required': 'Please enter your full name.',
                'invalid': 'Please enter a valid name.',
            },
            'phone_number': {
                'required': 'Phone number is required.',
            },
            'date': {
                'required': 'Please select a reservation date.',
                'invalid': 'Enter a valid date.',
            },
            'time': {
                'required': 'Please select a reservation time.',
                'invalid': 'Enter a valid time.',
            },
            'guests_count': {
                'required': 'Please enter the number of guests.',
                'invalid': 'Enter a valid number.',
                'min_value': 'There must be at least 1 guest.',
            },
            'tables': {
                'required': 'Please select at least one table.',
            },
        }

    def clean_customer_name(self):
        name = self.cleaned_data.get('customer_name')
        value = name.split(' ')

        if len(value) != 2:
            raise forms.ValidationError(
                'Enter your first and last name separated by one space.'
            )

        if any(len(part) < 2 for part in value):
            raise forms.ValidationError(
                'First and last name must contain at least 2 letters each.'
            )

        if not all(part.isalpha() for part in value):
            raise forms.ValidationError(
                'Name must contain only letters.'
            )

        return name



    def clean(self):
        cleaned_data = super().clean()

        date = cleaned_data.get('date')
        time = cleaned_data.get('time')
        guests_count = cleaned_data.get('guests_count')
        tables = cleaned_data.get('tables')

        if date and time:
            start = datetime.combine(date, time)
            end = start + timedelta(hours=2)
            now = timezone.localtime().replace(tzinfo=None)

            if start <= now:
                self.add_error('date', 'Reservation cannot be in the past.')

        if tables:
            for table in tables:
                if not table.in_service:
                    self.add_error('tables', 'One or more tables are out of service.')
                    break

            if guests_count:
                total_capacity = sum(table.capacity for table in tables)

                if total_capacity < guests_count:
                    self.add_error('tables', 'Not enough capacity for all guests.')

        if date and time and tables:
            reservations = Reservation.objects.filter(
                tables__in=tables,
                status='confirmed',
                date__range=((start - timedelta(hours=2)).date(), end.date())
            ).exclude(pk=self.instance.pk).distinct()

            for reservation in reservations:
                reserved_start = datetime.combine(reservation.date, reservation.time)
                reserved_end = reserved_start + timedelta(hours=2)

                if start < reserved_end and end > reserved_start:
                    self.add_error('tables', 'One or more tables are already reserved.')
                    break

        return cleaned_data 

