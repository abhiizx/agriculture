from django.urls import path, include
from . import views



urlpatterns = [
    path('', views.index, name='home'),
    path('navbar/', views.index, name='navbar'),
    path('accounts/', include('accounts.urls')),  # including accounts app's URLs 
    path('search/', views.search_results, name='search_results'),
    path('search/', views.search, name='search'),

]
