from django.urls import path
from project_apps.menu import views


urlpatterns = [
    path('dishes/',views.DishListView.as_view(),name='dish_list'),
    path('dishes/<int:pk>/',views.DishDetailView.as_view(),name='dish_detail'),
    path('dishes/create/',views.DishCreateView.as_view(),name='dish_create'),
    path('dishes/<int:pk>/update/',views.DishUpdateView.as_view(),name='dish_update'),
    path('dishes/<int:pk>/delete/',views.DishDeleteView.as_view(),name='dish_delete'),
]