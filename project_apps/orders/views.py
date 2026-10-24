from django.shortcuts import render
from django.urls import reverse_lazy
from project_apps.orders.forms import OrderUpdateForm, OrderForm
from project_apps.orders.models import Order
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView


class OrderListView(ListView):
    model = Order
    template_name = 'orders/orders_list.html'
    context_object_name = 'orders'
    paginate_by = 10
    ordering = ['-created_at']


class OrderDetailView(DetailView):
    model = Order
    template_name = 'orders/orders_detail.html'
    context_object_name = 'order'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_price'] = sum(dish.price for dish in self.object.dishes.all())

        return context


class OrderCreateView(CreateView):
    model = Order
    form_class = OrderForm
    template_name = 'orders/orders_form.html'
    success_url = reverse_lazy('orders_list')


class OrderUpdateView(UpdateView):
    model = Order
    form_class = OrderUpdateForm
    template_name = 'orders/orders_form.html'
    success_url = reverse_lazy('orders_list')


class OrderDeleteView(DeleteView):
    model = Order
    template_name = 'orders/order_confirm_delete.html'
    success_url = reverse_lazy('orders_list')
    context_object_name = 'order'


