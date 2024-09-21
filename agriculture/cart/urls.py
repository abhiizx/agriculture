from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('detail/', views.cart_detail, name='cart_detail'),
    path('view/', views.cart_view, name='cart_view'),  # Updated to be consistent with 'cart_view' function
    path('create/', views.create_cart, name='create_cart'),
    path('remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
]
