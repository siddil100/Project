from django.urls import path
from . import views
from destmanager.views import MyPasswordChangeView



app_name = 'destmanager'


urlpatterns = [

    path('password_change/', MyPasswordChangeView.as_view(), name='password_change'),
    path('eventhome/', views.eventhome, name='eventhome'),
    path('package-bookings/', views.package_booking_list, name='package_booking_list'),
    path('view-package/<int:package_id>/', views.view_package, name='view_package'),
    path('package/<int:pk>/edit/', views.edit_package, name='edit_package'),
    path('addfood/', views.add_food_item, name='addfood'),
    path('adddecorations/', views.add_decorations, name='add_decor'),
    path('addevents/', views.add_events, name='addevents'),
    path('upload/', views.upload_license, name='upload_license'),
    path('check-phone/', views.check_phone_number, name='check_phone_number'),

]
