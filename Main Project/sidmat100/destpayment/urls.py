from django.urls import path
from . import views


app_name = 'destpayment'


urlpatterns = [


    path('book_package/<int:package_id>/', views.book_package, name='book_package'),
    path('custom_bookpackage/<int:package_id>/', views.custom_bookpackage, name='custom_bookpackage'),
   
    path('success/', views.payment_success, name='payment_success'),
    path('customsuccess/', views.custompayment_success, name='custompayment_success'),

    path('render-payment-success/', views.render_payment_success, name='render_payment_success'),
    path('render-custompayment-success/', views.render_custompayment_success, name='render_custompayment_success'),
    path('download-pdf/', views.download_pdf, name='download_pdf'),
    path('download-custompdf/', views.download_custompdf, name='download_custompdf'),
    path('proceed_tocustom/', views.proceed_tocustom, name='proceed_tocustom'),
    path('custompackage/', views.custom_package, name='custompackage'),
    path('get_decor_price/', views.get_decor_price, name='get_decor_price'),
    path('get_event_price/', views.get_event_price, name='get_event_price'),
    path('get_food_price/', views.get_food_price, name='get_food_price'),
   

]
