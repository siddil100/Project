from django.urls import path
from . import views
from .views import MyPasswordChangeView

app_name = 'accounts'

urlpatterns = [
    path('', views.login_view, name='login'),
    
    path('register/', views.register, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('password_change/', MyPasswordChangeView.as_view(), name='password_change'),
]