
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from project_apps.menu.forms import DishForm
from project_apps.menu.models import Dish
from django.contrib import messages
from django.shortcuts import redirect


class DishListView(ListView):
    model = Dish
    template_name = 'menu/dish_list.html'
    context_object_name = 'dishes'
    paginate_by = 10
    ordering = ['category','name']

    def get_queryset(self):
        value = super().get_queryset()
        cat = self.request.GET.get('category')
        if cat :
            return value.filter(category=cat)

        return value



class DishDetailView(DetailView):
    model = Dish
    template_name = 'menu/dish_detail.html'
    context_object_name = 'dish'


class DishCreateView(CreateView):
    model = Dish
    form_class = DishForm
    template_name = 'menu/dish_form.html'
    success_url = reverse_lazy('dish_list')


class DishUpdateView(UpdateView):
    model = Dish
    form_class = DishForm
    template_name = 'menu/dish_form.html'
    success_url = reverse_lazy('dish_list')


class DishDeleteView(DeleteView):
    model = Dish
    template_name = 'menu/dish_confirm_delete.html'
    success_url = reverse_lazy('dish_list')
    context_object_name = 'dish'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['has_orders'] = self.object.orders.exists()

        return context

    def form_valid(self, form):
        if self.object.orders.exists():
            messages.error(self.request,'This dish is included in ongoing orders and cannot be deleted.')
            return redirect('dish_detail', pk=self.object.pk)

        return super().form_valid(form)


