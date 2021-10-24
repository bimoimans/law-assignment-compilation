from django.shortcuts import render
from django.http import  HttpResponse, HttpResponseRedirect, FileResponse

import requests
import random
import json

from .forms import FileForm

#TODO Receive file, return to sender

# Create your views here.
def open_page(request):
    form = FileForm()
    return render(request, "form.html", {'form': form})

def send_file_show_result(request):
    url = "http://localhost:8030/compress/"
    routing_key = str(random.randint(1000, 9999))
    headers = {'x-routing-key' : routing_key}
    mess = "defaultnya fail"
    if request.method == "POST":
        form = FileForm(request.POST, request.FILES)
        if form.is_valid():
            #print(request.FILES['uploaded_file'])
            files = request.FILES['uploaded_file']
            openfile = files.read()
            sent_file = {'uploaded_file': (files.name, openfile)}
            r = requests.post(url, files = sent_file, headers = headers)
            mess = r.json()
        return render(request, "res.html", {"message": mess, "routing": routing_key})
