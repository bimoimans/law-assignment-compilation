# -*- coding: utf-8 -*-
from django.urls import path 
from . import views
  
urlpatterns = [
    path('compress/', views.compress_file),
    path('delall/', views.del_all)
]