from django.urls import path

from .views import add_robot


app_name = 'api'

urlpatterns = [
    path('add_robot/', add_robot, name='add_robot'),
]
