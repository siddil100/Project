from django.urls import path
from . import views


app_name = 'destmanager'


urlpatterns = [


    path('eventhome/', views.eventhome, name='eventhome'),
    path('package-bookings/', views.package_booking_list, name='package_booking_list'),
    path('view-package/<int:package_id>/', views.view_package, name='view_package'),
    path('package/<int:pk>/edit/', views.edit_package, name='edit_package'),

]
