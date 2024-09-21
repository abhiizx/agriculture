from django.db import models
from products.models import Product

class Cart(models.Model):
    products = models.ManyToManyField(Product, through='CartItem')

    def add_product(self, product, quantity):
        if not isinstance(product, Product):
            raise ValueError("Expected a Product instance")

        if quantity <= 0:
            raise ValueError("Quantity must be greater than zero")

        # Get or create the CartItem instance
        cart_item, created = CartItem.objects.get_or_create(cart=self, product=product)

        # Check if adding the requested quantity exceeds available stock
        if (cart_item.quantity + quantity) > product.quantity:
            raise ValueError(f"Cannot add {quantity} of {product.name}. Only {product.quantity - cart_item.quantity} available.")

        if created:
            # New item created
            cart_item.quantity = quantity
        else:
            # Item already exists, update quantity
            cart_item.quantity += quantity

        if cart_item.quantity <= 0:
            # If quantity is zero or less, delete the cart item
            cart_item.delete()
        else:
            # Save the updated cart item
            cart_item.save()

    def total_price(self):
        # Calculate the total price of items in the cart
        return sum(item.product.price * item.quantity for item in self.cartitem_set.all())

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)  # Ensure quantity has a default value of 1
