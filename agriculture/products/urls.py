from django.urls import path
from . import views
from .views import product_list_by_category


urlpatterns = [
    path('add-product/', views.add_product, name='add_product'),
    path('product-list/', views.product_list, name='product_list'),
    path('product-details/<int:pk>/', views.product_details, name='product_details'),  # Product details page
    path('payment/<int:product_id>/', views.payment, name='payment'),
    path('payment/success/', views.payment_success, name='payment_success'),
    
    # product category
    path('flower-seeds/', views.flower_seeds, name='flower_seeds'),
    path('fruit-seeds/', views.fruit_seeds, name='fruit_seeds'),
    path('plants/', views.plants, name='plants'),
    path('herbs-seeds/', views.herbs_seeds, name='herbs_seeds'),
    path('vegitable-seeds/', views.vegitable_seeds, name='vegitable_seeds'),

    path('category/<slug:category_slug>/', product_list_by_category, name='product_list_by_category'),

]
