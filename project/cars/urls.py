from django.urls import path
from .views import (
    car_list,
    car_detail,
    car_create,
    car_update,
    car_delete,
    register,
)


urlpatterns = [
    path('', car_list, name='car_list'),
    path('cars/<int:car_id>/', car_detail, name='car_detail'),
    path('cars/create/', car_create, name='car_create'),
    path('cars/<int:car_id>/edit/', car_update, name='car_update'),
    path('cars/<int:car_id>/delete/', car_delete, name='car_delete'),
    path('register/', register, name='register'),
]
