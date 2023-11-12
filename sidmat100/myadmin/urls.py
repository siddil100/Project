from django.urls import path
from . import views

app_name = 'myadmin'

urlpatterns = [
   
    
    
    path('myadmin/', views.myadminview, name='myadmin'),
    path('aadharsus/', views.aadharsusview, name='aadharsus'),
    path('generate_pdf/<int:user_id>/',views.generate_pdf, name='generate_pdf'),
    
]