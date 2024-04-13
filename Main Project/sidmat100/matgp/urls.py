from django.urls import path
from . import views




app_name = 'matgp' 

urlpatterns = [
    # Other paths for your app...
    path('detect_faces/', views.detect_faces, name='detect_faces'),
    
   
    
]