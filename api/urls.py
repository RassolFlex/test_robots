from django.urls import path

from .views import add_robot, download_production_list


app_name = 'api'

urlpatterns = [
    path('add_robot/', add_robot, name='add_robot'),
    path('download_production_list/', download_production_list,
         name='download_production_list'),
]
