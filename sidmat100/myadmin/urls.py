from django.urls import path
from . import views

app_name = 'myadmin'

urlpatterns = [
   
    
    
    path('myadmin/', views.myadminview, name='myadmin'),
    
]