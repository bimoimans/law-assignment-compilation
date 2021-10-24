from django.db import models

# Create your models here.
class UploadedFile(models.Model):
    uploaded_file = models.FileField(upload_to='uploaded_file/')

class CompressedFile(models.Model):
    compressed_file = models.FileField(upload_to='compressed_file/')