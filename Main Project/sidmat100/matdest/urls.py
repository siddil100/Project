# matdest/urls.py

from django.urls import path
from . import views


app_name = 'matdest'


urlpatterns = [
    path('desthome/', views.desthome, name='desthome'),
    path('my_custom_packages/', views.custom_package_bookings, name='my_custom_packages'),
    path('view_packages/', views.view_packages, name='view_packages'),
    path('view_package_details/<int:package_id>/', views.view_package_details, name='view_package_details'),
    path('view_mypackage_details/<int:package_id>/', views.view_mypackage_details, name='view_mypackage_details'),
    path('view_custom_package_details/<int:booking_id>/', views.view_custom_package_details, name='view_custom_package_details'),
    path('chatbot/', views.chatbot_redirect, name='chatbot_redirect'),
    path('my-packages/', views.view_my_packages, name='my_packages'),
     path('get_package_location/', views.get_package_location, name='get_package_location'),
    path('check_booking_limit/', views.check_booking_limit, name='check_booking_limit'),


    path('generate_pdf_report/', views.generate_user_report, name='generate_user_report'),
]
