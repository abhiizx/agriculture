from django.db import models
from django.utils.text import slugify

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)  # Automatically create a slug from the name
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField(default=0)  # Stock quantity of the product
    image = models.ImageField(upload_to='products/')  # Ensure media settings are configured
    available = models.BooleanField(default=True)  # Indicates if the product is available for sale
    category = models.ForeignKey(Category, on_delete=models.CASCADE)  # Link to category
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=0.0)  # New field for rating

    def __str__(self):
        return self.name
