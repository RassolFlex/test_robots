from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('api/', include('api.urls', namespace='api')),
    path('admin/', admin.site.urls),
    path('add_order/', include('orders.urls', namespace='orders')),
]
