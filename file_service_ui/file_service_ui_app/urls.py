# -*- coding: utf-8 -*-
from django.urls import path 
from . import views
  
urlpatterns = [
    path('form/', views.open_page, name='upload_form'),
    path('send/', views.send_file_show_result, name='send_file'),
    #path('receive/', views.)
]