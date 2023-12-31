from django.urls import path
from . import views

app_name = 'matrimony'

urlpatterns = [
   
    
    path('personaldetails', views.personaldetailsview, name='personaldetails'),
    path('familydetails', views.familydetailsview, name='familydetails'),
    path('educationaldetails', views.educationaldetailsview, name='educationaldetails'),
    path('employmentdetails', views.employmentdetailsview, name='employmentdetails'),
    path('locationdetails', views.locationdetailsview, name='locationdetails'),
    path('physicaldetails', views.physicaldetailsview, name='physicaldetails'),
    path('home', views.homeview, name='home'),
    path('check_phone_number/', views.check_phone_number, name='checkphone'),
    path('profile/<int:user_id>/', views.user_detail, name='user_detail'),
    path('myprofile', views.myprofileview, name='myprofile'),
    path('update_personaldetails', views.update_personaldetails, name='update_personaldetails'),
    path('update_familydetails', views.update_familydetails, name='update_familydetails'),
    path('update_educationaldetails', views.update_educationaldetails, name='update_educationaldetails'),
    path('update_employmentdetails', views.update_employmentdetails, name='update_employmentdetails'),
    path('update_locationdetails', views.update_locationdetails, name='update_locationdetails'),
    path('update_physicaldetails', views.update_physicaldetails, name='update_physicaldetails'),
    path('verify_email/<str:token>/', views.verify_email_view, name='verify_email'),
    path('update_aadhar', views.update_aadhar, name='update_aadhar'),
    path('upload_images', views.upload_images, name='upload_images'),
    path('edit_image/<int:image_upload_id>/<int:image_id>/', views.edit_image, name='edit_image'),
    path('delete_image/<int:image_upload_id>/<int:image_id>/', views.delete_image, name='delete_image'),
    path('update-preference/', views.update_preference, name='update_preference'),
    path('block_user/<int:user_id>/', views.block_user, name='block_user'),
    path('blocked_users/', views.blocked_users_list, name='blocked_users_list'),
    path('unblock_user/<int:user_id>/', views.unblock_user, name='unblock_user'),

    
]