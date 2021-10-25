from django.shortcuts import render, resolve_url
from django.http import  HttpResponse, HttpResponseRedirect

import requests

from django.views.decorators.csrf import csrf_exempt
# Create your views here.
def open_signin_page(request):
    return render(request, "signin.html", {'endpoint': 'http://localhost:8000/chat_room/handle_signin/', 'button_text':"sign in"})

def open_signup_page(request):
    return render(request, "signin.html", {'endpoint': 'http://localhost:8000/auth/users/?format=json', 'button_text':"sign up"})

@csrf_exempt
def sign_in_handler(request):
    if request.method == "POST":
        url = "http://localhost:8000/auth/token/login/?format=json"
        username = request.POST["username"]
        password = request.POST["password"]
        payload = {"username": username,
                   "password": password}
        requested_token = requests.post(url, data=payload).json()
        request.session["access_token"] = requested_token["auth_token"]
    return HttpResponseRedirect('http://localhost:8000/chat_room/chats/list/')

def print_session(request):
    print(request.session.get("access_token",0))
    return HttpResponseRedirect('http://localhost:8000/chat_room/chats/list')

def sign_up_handler(request):
    return
# def signin(request):
#     return request

# def signup(request):
#     return request