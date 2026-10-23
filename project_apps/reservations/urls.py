from django.urls import path
from project_apps.reservations import views

table_patterns = [
    path('tables/', views.TableListView.as_view(), name='table_list'),
    path('tables/<int:pk>/', views.TableDetailView.as_view(), name='table_detail'),
    path('tables/create/', views.TableCreateView.as_view(), name='table_create'),
    path('tables/<int:pk>/update/', views.TableUpdateView.as_view(), name='table_update'),
    path('tables/<int:pk>/delete/', views.TableDeleteView.as_view(), name='table_delete'),
]



reservation_patterns = [
    path('list/', views.ReservationListView.as_view(), name='reservation_list'),
    path('<int:pk>/', views.ReservationDetailView.as_view(), name='reservation_detail'),
    path('create/', views.ReservationCreateView.as_view(), name='reservation_create'),
    path('<int:pk>/update/', views.ReservationUpdateView.as_view(), name='reservation_update'),
    path('<int:pk>/delete/', views.ReservationDeleteView.as_view(), name='reservation_delete'),
]


urlpatterns = table_patterns + reservation_patterns