# matdest/urls.py

from django.urls import path
from . import views


app_name = 'matdest'


urlpatterns = [
    path('desthome/', views.desthome, name='desthome'),
    path('view_packages/', views.view_packages, name='view_packages'),
]
