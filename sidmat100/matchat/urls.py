

from django.urls import path
from . import views



app_name = 'matchat'

urlpatterns = [
    path('chat/<int:receiver_id>/', views.chat, name='chat'),
    path('get_messages/<int:receiver_id>/', views.get_messages, name='get_messages'),
    path('send_message/<int:receiver_id>/', views.send_message, name='send_message'),
    path('mychats/', views.mychats, name='mychats'),

    # Add other URLs as needed
]
