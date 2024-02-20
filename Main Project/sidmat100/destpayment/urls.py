from django.urls import path
from . import views


app_name = 'destpayment'


urlpatterns = [


    path('book_package/<int:package_id>/', views.book_package, name='book_package'),
    path('process_booking_payment/', views.process_booking_payment, name='process_booking_payment'),
    path('success/', views.payment_success, name='payment_success'),
   

]
