from django.shortcuts import render, get_object_or_404, redirect
from .models import Cart, CartItem
from products.models import Product
import logging
from django.contrib import messages


logger = logging.getLogger(__name__)

def add_to_cart(request, product_id):
    cart_id = request.session.get('cart_id')

    # Create a new cart if none exists
    if not cart_id:
        cart = Cart.objects.create()
        request.session['cart_id'] = cart.id
    else:
        cart = get_object_or_404(Cart, id=cart_id)

    product = get_object_or_404(Product, id=product_id)

    try:
        # Get the quantity from the request, default is 1
        quantity = int(request.POST.get('quantity', 1))

        # Ensure quantity is greater than zero
        if quantity <= 0:
            raise ValueError("Quantity must be greater than zero")

        # Check if enough stock is available
        if product.quantity < quantity:  # Change here to use product.quantity
            messages.error(request, f"Only {product.quantity} units available for {product.name}.")
            return redirect('cart:cart_view')

        # Add the product to the cart
        cart.add_product(product, quantity)

        # Update the product quantity (stock)
        product.quantity -= quantity  # Change here to use product.quantity
        product.save()

    except ValueError as e:
        # Log the exception
        logger.error(f"Error adding product to cart: {e}")
        # Optionally: redirect to an error page or display a message
        messages.error(request, "Invalid quantity.")
        return redirect('cart:cart_view')

    # Redirect to the cart view after successfully adding the product
    return redirect('cart:cart_view')

def create_cart(request):
    cart = Cart.objects.create()
    request.session['cart_id'] = cart.id
    return redirect('cart:cart_detail')

def cart_view(request):
    cart_id = request.session.get('cart_id')
    if cart_id:
        cart = get_object_or_404(Cart, id=cart_id)
    else:
        cart = None  # No cart in session, so no cart to display
    
    return render(request, 'cart/cart_view.html', {'cart': cart})

def cart_detail(request):
    cart_id = request.session.get('cart_id')
    if cart_id:
        cart = get_object_or_404(Cart, id=cart_id)
    else:
        cart = None  # No cart in session, so no cart to display
    
    return render(request, 'cart/cart_detail.html', {'cart': cart})


def remove_from_cart(request, item_id):
    cart = Cart.objects.get(id=request.session['cart_id'])  # Get the cart using the session ID
    item = get_object_or_404(CartItem, id=item_id, cart=cart)  # Get the specific CartItem

    item.delete()  # Remove the item from the cart
    return redirect('cart:cart_view')  # Redirect back to the cart detail page