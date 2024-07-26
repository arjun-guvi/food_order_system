from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('foods/', views.food_list, name='food_list'),
    path('foods/<int:pk>/', views.food_detail, name='food_detail'),
    path('foods/new/', views.food_create, name='food_create'),
    path('foods/<int:pk>/edit/', views.food_update, name='food_update'),
    path('foods/<int:pk>/delete/', views.food_delete, name='food_delete'),
    path('orders/', views.order_list, name='order_list'),
    path('orders/<int:pk>/', views.order_detail, name='order_detail'),
    path('orders/new/', views.order_create, name='order_create'),
    path('orders/<int:pk>/delete/', views.order_delete, name='order_delete'),
]
