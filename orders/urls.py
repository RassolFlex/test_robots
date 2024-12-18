from django.urls import path

from orders.views import add_order


app_name = 'orders'

urlpatterns = [
    path('', add_order, name='add_order'),
]
