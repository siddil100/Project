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
     path('search/', views.search_view, name='search_page'),
     path('global-search/', views.global_search, name='global_search'),
     path('add_interested/<int:user_id>/', views.add_interested, name='add_interested'),
     path('interested_profiles/', views.interested_profiles_list, name='interested_profiles_list'),
     path('remove_interest_profiles/<int:user_id>/', views.remove_interest_profiles, name='remove_interest_profiles'),
     path('add_notinterested/<int:user_id>/', views.add_notinterested, name='add_notinterested'),
    path('notinterested_list/', views.notinterested_list, name='notinterested_list'),
    path('remove_notinterested/<int:user_id>/', views.remove_notinterested, name='remove_notinterested'),
     
 

]
