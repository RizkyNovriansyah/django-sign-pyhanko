from django.db import models

# Create your models here.
class SignModel(models.Model):
    file = models.FileField(upload_to='file')