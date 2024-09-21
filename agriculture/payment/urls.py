from django.urls import path, include
from . import views

app_name = 'payment'

urlpatterns = [
    path('checkout/', views.checkout, name='checkout'),
]
