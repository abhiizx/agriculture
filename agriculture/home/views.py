from django.shortcuts import render
from django.shortcuts import render
from products.models import Product 


def index(request):
    return render(request, 'home/index.html')


def search(request):
    query = request.GET.get('q')
    products = Product.objects.filter(name__icontains=query) if query else []
    return render(request, 'home/search_results.html', {'products': products, 'query': query})

def search_results(request):
    query = request.GET.get('q', '')
    results = Product.objects.filter(name__icontains=query)  # Adjust the field as needed
    return render(request, 'home/search_results.html', {'results': results, 'query': query})