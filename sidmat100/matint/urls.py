from django.urls import path
from . import views


from django.urls import path

app_name = 'matint'


urlpatterns = [
    # Other URL patterns...
     path('send-interest/<int:user_id>/', views.send_interest, name='send_interest'),
     path('received-interests/', views.received_interests, name='received_interests'),
     path('accept-interest/<int:interest_id>/', views.accept_interest, name='accept_interest'),
     path('reject-interest/<int:interest_id>/', views.reject_interest, name='reject_interest'),
]
