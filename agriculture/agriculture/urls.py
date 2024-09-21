from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')), 
    path('accounts/', include('accounts.urls')),             # account app's URLs
    path('products/', include('products.urls')),             # product app's URLs
    path('cart/', include('cart.urls', namespace='cart')),   # cart app's URLs
    path('payment/', include('payment.urls')),               # payment app's URLs
    
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

