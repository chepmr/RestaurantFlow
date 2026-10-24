
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from project_apps.reservations.forms import TableForm, ReservationForm, ReservationUpdateForm
from project_apps.reservations.models import Table, Reservation
from datetime import datetime, timedelta
from django.contrib import messages
from django.shortcuts import redirect
from django.utils import timezone


class TableListView(ListView):
    model = Table
    template_name = 'reservations/for_table/table_list.html'
    context_object_name = 'tables'
    paginate_by = 10
    ordering = ['number']

class TableDetailView(DetailView):
    model = Table
    template_name = 'reservations/for_table/table_detail.html'
    context_object_name = 'table'

class TableCreateView(CreateView):
    model = Table
    form_class = TableForm
    template_name = 'reservations/for_table/table_form.html'
    success_url = reverse_lazy('table_list')




class TableUpdateView(UpdateView):
    model = Table
    form_class = TableForm
    template_name = 'reservations/for_table/table_form.html'
    success_url = reverse_lazy('table_list')

    def form_valid(self, form):
        old_in_service = Table.objects.get(pk=self.object.pk).in_service
        going_out_of_service = (old_in_service and not form.cleaned_data['in_service'])

        has_reservations = False

        if going_out_of_service:
            now = timezone.localtime()
            earliest_date = (now - timedelta(hours=2)).date()

            reservations = self.object.reservations.filter(status='confirmed',date__gte=earliest_date)

            for reservation in reservations:
                start = timezone.make_aware(datetime.combine(reservation.date, reservation.time),timezone.get_current_timezone())

                if start + timedelta(hours=2) > now:
                    has_reservations = True
                    break

        response = super().form_valid(form)

        if has_reservations:
            messages.warning(self.request,'This table has active or upcoming reservations. ''Please review them and assign another table if necessary.')

        return response



class TableDeleteView(DeleteView):
    model = Table
    template_name = 'reservations/for_table/table_confirm_delete.html'
    success_url = reverse_lazy('table_list')
    context_object_name = 'table'

    def has_active_reservations(self):
        now = timezone.localtime()
        earliest_date = (now - timedelta(hours=2)).date()

        reservations = self.object.reservations.filter(
            status='confirmed',
            date__gte=earliest_date
        )

        for reservation in reservations:
            start = timezone.make_aware(datetime.combine(reservation.date, reservation.time),timezone.get_current_timezone())

            if start + timedelta(hours=2) > now:
                return True

        return False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['has_active_reservations'] = self.has_active_reservations()
        context['has_orders'] = self.object.orders.exists()

        return context

    def form_valid(self, form):
        if self.object.orders.exists():
            messages.error(self.request,'This table has existing orders and cannot be deleted.')
            return redirect('table_detail', pk=self.object.pk)

        if self.has_active_reservations():
            messages.error(self.request,'This table has an active or upcoming reservation and cannot be deleted.')
            return redirect('table_detail', pk=self.object.pk)

        return super().form_valid(form)


class ReservationListView(ListView):
    model = Reservation
    template_name = 'reservations/for_reservation/reservation_list.html'
    context_object_name = 'reservations'
    paginate_by = 10
    ordering = ['date', 'time']


class ReservationDetailView(DetailView):
    model = Reservation
    template_name = 'reservations/for_reservation/reservation_detail.html'
    context_object_name = 'reservation'


class ReservationCreateView(CreateView):
    model = Reservation
    form_class = ReservationForm
    template_name = 'reservations/for_reservation/reservation_form.html'
    success_url = reverse_lazy('reservation_list')


class ReservationUpdateView(UpdateView):
    model = Reservation
    form_class = ReservationUpdateForm
    template_name = 'reservations/for_reservation/reservation_form.html'
    success_url = reverse_lazy('reservation_list')


class ReservationDeleteView(DeleteView):
    model = Reservation
    template_name = 'reservations/for_reservation/reservation_confirm_delete.html'
    success_url = reverse_lazy('reservation_list')
    context_object_name = 'reservation'