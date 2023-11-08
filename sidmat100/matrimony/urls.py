from django.urls import path
from . import views

app_name = 'matrimony'

urlpatterns = [
   
    
    path('personaldetails', views.personaldetailsview, name='personaldetails'),
    path('familydetails', views.familydetailsview, name='familydetails'),
    path('educationaldetails', views.educationaldetailsview, name='educationaldetails'),
    path('employmentdetails', views.employmentdetailsview, name='employmentdetails'),
    path('locationdetails', views.locationdetailsview, name='locationdetails'),
    path('home', views.homeview, name='home'),
    path('check_phone_number/', views.check_phone_number, name='checkphone'),
    path('profile/<int:user_id>/', views.user_detail, name='user_detail'),
    path('myprofile', views.myprofileview, name='myprofile'),
    path('update_personaldetails', views.update_personaldetails, name='update_personaldetails'),

    
]