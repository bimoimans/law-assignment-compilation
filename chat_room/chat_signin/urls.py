"""URL's for the chat app."""

from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('signin/', views.open_signin_page),
    path('signup/', views.open_signup_page),
    path('cek/', views.print_session),
    path('handle_signin/', views.sign_in_handler)
]