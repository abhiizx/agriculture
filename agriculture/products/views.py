from django.shortcuts import render, redirect, get_object_or_404
from .forms import ProductForm
from .models import Category, Product
from django.http import HttpResponse
import razorpay
from django.conf import settings

def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()  # Save the product to the database
            
            # After saving, redirect to the category page of this product
            return redirect('product_list_by_category', category_slug=product.category.slug)
    else:
        form = ProductForm()

    return render(request, 'products/add_product.html', {'form': form})

def product_list(request):
    products = Product.objects.all()  # Fetch all products from the database
    return render(request, "products/product_list.html", {'products': products})

def product_details(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'products/product_details.html', {'product': product})

def payment(request, product_id):
    product = Product.objects.get(id=product_id)
    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

    # Razorpay order creation
    order_amount = int(product.price * 100)  # Amount in paise (multiply by 100)
    order_currency = 'INR'
    order_receipt = f'order_{product_id}'
    razorpay_order = client.order.create({
        "amount": order_amount,
        "currency": order_currency,
        "receipt": order_receipt,
        "payment_capture": 1
    })

    context = {
        'product': product,
        'order_id': razorpay_order['id'],
        'razorpay_key_id': settings.RAZORPAY_KEY_ID,
        'amount': order_amount,
    }
    return render(request, 'payment/payment.html', context)

def payment_success(request):
    payment_id = request.POST.get('razorpay_payment_id')
    order_id = request.POST.get('razorpay_order_id')
    signature = request.POST.get('razorpay_signature')

    # Verify payment signature
    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
    params_dict = {
        'razorpay_order_id': order_id,
        'razorpay_payment_id': payment_id,
        'razorpay_signature': signature
    }
    
    try:
        client.utility.verify_payment_signature(params_dict)
        # Payment successful, handle post-payment logic (e.g., saving transaction, updating order status)
        return HttpResponse("Payment was successful!")
    except razorpay.errors.SignatureVerificationError:
        return HttpResponse("Payment verification failed.")
    
def flower_seeds(request):
    return render(request, 'category/flower_seeds.html')

def fruit_seeds(request):
    return render(request, 'category/fruit_seeds.html')

def herbs_seeds(request):
    return render(request, 'category/herbs_seeds.html')

def plants(request):
    return render(request, 'category/plants.html')

def vegitable_seeds(request):
    return render(request, 'category/vegitable_seeds.html')

def product_list_by_category(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    products = Product.objects.filter(category=category)
    
    return render(request, 'category/category_products.html', {
        'category': category,
        'products': products
    })

