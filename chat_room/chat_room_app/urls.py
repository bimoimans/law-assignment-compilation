"""URL's for the chat app."""

from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('delall/', views.del_all_chat_room),
    path('chats/', views.ChatSessionView.as_view()),
    path('chats/list/', views.chat_room_list),
    path('chats/createnew/', views.handle_create_new_chatroom),
    path('chats/send/', views.send_message),
    path('chats/<uri>/', views.ChatSessionView.as_view()),
    path('chats/<uri>/messages/', views.ChatSessionMessageView.as_view()),
    
]