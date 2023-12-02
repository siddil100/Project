from django.urls import path
from . import views




app_name = 'matpayment' 


urlpatterns = [
    # Other paths for your app...
    path('upgrade/', views.upgrade_to_premium, name='upgrade_to_premium'),
    path('success/', views.paymentsuccess, name='paymentsuccess'),
    path('view_premium/', views.view_premium, name='view_premium'),
    
]