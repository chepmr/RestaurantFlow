from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from project_apps.menu.forms import DishForm
from project_apps.menu.models import Dish


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


