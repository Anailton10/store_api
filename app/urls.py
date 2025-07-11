from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('accounts.urls')),
    path('api/v1/', include('products.urls')),
    path('api/v1/', include('carts.urls')),
    path('api/', include('authentication.urls')),
]
