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
    path('adview_packages/', views.adview_packages, name='adview_packages'),
    path('package/<int:pk>/edit/', views.edit_package, name='edit_package'),
    path('package/<int:pk>/delete/',views.delete_package, name='delete_package'),
    path('add-manager/', views.add_manager, name='add_manager'),
    path('view-manager/', views.view_manager, name='view_manager'),
    path('suspend-manager/<int:user_id>/', views.suspend_manager, name='suspend_manager'),
   
    path('licenses/', views.license_list, name='license_list'),
    path('licenses/approve/<int:license_id>/', views.approve_license, name='approve_license'),
    path('licenses/decline/<int:license_id>/', views.decline_license, name='decline_license'),
    path('api/get-subcategories/', views.get_subcategories, name='get_subcategories'),
    path('api/get-subtypes/', views.get_decoration_subtypes, name='get_decoration_subtypes'),
    path('api/get-price/', views.get_price, name='get_price'),
   
    

    
]