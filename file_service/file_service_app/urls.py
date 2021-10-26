# -*- coding: utf-8 -*-
from django.urls import path 
from . import views
from django.conf.urls.static import static
from django.conf import settings
  
urlpatterns = [
    path('compress/', views.compress_file),
    path('delall/', views.del_all)
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)