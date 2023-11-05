from django.urls import path
from . import views

app_name = 'matrimony'

urlpatterns = [
   
    
    path('personaldetails', views.personaldetailsview, name='personaldetails'),
    path('familydetails', views.familydetailsview, name='familydetails'),
    path('check_phone_number/', views.check_phone_number, name='checkphone'),
    
]