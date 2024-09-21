from django.contrib import admin
from .models import Product, Category

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'price', 'quantity','image','category')  # Adjust fields as needed
    search_fields = ('name', 'description')

admin.site.register(Category)
