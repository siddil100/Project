from django.urls import path
from . import views

app_name = 'myadmin'

urlpatterns = [
   
    
    
    path('myadmin/', views.myadminview, name='myadmin'),
    path('aadharsus/', views.aadharsusview, name='aadharsus'),
    path('generate_pdf/<int:user_id>/',views.generate_pdf, name='generate_pdf'),
    path('profile_admin/<int:user_id>/', views.user_detail_admin, name='user_detail_admin'),
    path('change_password_admin/', views.change_password_admin, name='change_password_admin'),
    path('view_premium/', views.premium_users_view, name='view_premium'),
    path('destadmin/', views.destadmin, name='destadmin'),
    path('add/', views.addpackage, name='add_package'),

    
]