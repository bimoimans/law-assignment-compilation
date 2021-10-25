from django.shortcuts import render, resolve_url

# Create your views here.
def open_signin_page(request):
    return render(request, "signin.html", {'endpoint': 'http://localhost:8000/auth/token/login/', 'button_text':"sign in"})

def open_signup_page(request):
    return render(request, "signin.html", {'endpoint': 'http://localhost:8000/auth/users/', 'button_text':"sign up"})

def cek_request(request):
    print(request)
    return render(request, "signin.html", {'endpoint': '/auth/token/login/', 'button_text':"sign in"})

# def signin(request):
#     return request

# def signup(request):
#     return request