from django.urls import path
from project_apps.orders import views


urlpatterns = [
    path('',views.OrderListView.as_view(),name='orders_list'),
    path('<int:pk>/',views.OrderDetailView.as_view(),name='order_detail'),
    path('create/',views.OrderCreateView.as_view(),name='order_create'),
    path('<int:pk>/update/',views.OrderUpdateView.as_view(),name='order_update'),
    path('<int:pk>/delete/',views.OrderDeleteView.as_view(),name='order_delete'),
]