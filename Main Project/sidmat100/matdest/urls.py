# matdest/urls.py

from django.urls import path
from . import views


app_name = 'matdest'


urlpatterns = [
    path('desthome/', views.desthome, name='desthome'),
    path('view_packages/', views.view_packages, name='view_packages'),
    path('view_package_details/<int:package_id>/', views.view_package_details, name='view_package_details'),
    path('chatbot/', views.chatbot_redirect, name='chatbot_redirect'),
    path('my-packages/', views.view_my_packages, name='my_packages'),
]
