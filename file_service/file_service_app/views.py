from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files import File
from django.conf import settings

from notifications.utils import notify
from notifications import default_settings as notifs_settings
from .models import UploadedFile, CompressedFile

import sys
import os
import gzip
import threading
import pika
import time
#TODO send to rabbitmq, print progress

# Create your views here.
@csrf_exempt
def compress_file(request):
    jsonres = {"response":404}
    if request.method == "POST":
        files = request.FILES['uploaded_file']
        instance = UploadedFile(uploaded_file=files)
        instance.save()
        filename = files.name
        jsonres = {"response": "{} received".format(filename)}
        x = threading.Thread(target=_compress_and_send_to_rabbitmq, 
                             args=(instance.uploaded_file.path, 
                                   request.META["HTTP_X_ROUTING_KEY"], 
                                   filename), 
                             daemon=True)
        x.start()
    return JsonResponse(jsonres)   



@csrf_exempt
def del_all(request):
    # UploadedFile.objects.all().delete()
    # CompressedFile.objects.all().delete()
    return HttpResponse()

def _compress_and_send_to_rabbitmq(filepath, routingkey, filename):
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='task_queue', durable=True)

    input_file = filepath
    input_size = os.path.getsize(input_file)
    chunk_size = input_size // 10
    written = 0

    with open(input_file,"rb") as fr,gzip.open(input_file+".gz","wb") as fw:
        while (written < 100):
            time.sleep(0.5)
            chunk = fr.read(chunk_size)
            fw.write(chunk)
            written += 10
            message = "Progress at {} percent".format(written)
            print("-"*50)
            notif_args = {
                'silent': True,
                'extra_data': {
                    'npm' : '1706039780',
                    'message': message,
                    'routing': routingkey
                }
            }
            notify(**notif_args, channels=['websocket'])
        fw.close()
        fr.close()
    compressed = open(fw.name, "rb")
    djangofile = File(compressed)
    compressed_model = CompressedFile()
    compressed_model.compressed_file.save(filename + ".gz", djangofile)
    compressed.close()
    notif_args = {
            'silent': True,
            'extra_data': {
                'npm' : '1706039780',
                'message': compressed_model.compressed_file.url,
                'routing': routingkey
            }
    }
    notify(**notif_args, channels=['websocket'])

        