
from django.contrib import admin
from django.urls import path
from django.urls import include
from restaurant_op_system.views import HomeView
urlpatterns = [
    path('admin/', admin.site.urls),
    path('reservations/', include('project_apps.reservations.urls')),
    path('', HomeView.as_view(), name='home'),
    path('menu/',include('project_apps.menu.urls')),
    path('orders/',include('project_apps.orders.urls')),

]

