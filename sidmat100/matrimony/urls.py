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
    path('update_familydetails', views.update_familydetails, name='update_familydetails'),
    path('update_educationaldetails', views.update_educationaldetails, name='update_educationaldetails'),
    path('update_employmentdetails', views.update_employmentdetails, name='update_employmentdetails'),
    path('update_locationdetails', views.update_locationdetails, name='update_locationdetails'),
    path('verify_email/<str:token>/', views.verify_email_view, name='verify_email'),

    
]