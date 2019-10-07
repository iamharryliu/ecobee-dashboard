from django.db import models
from django.contrib.auth.models import User


class App(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    api_key = models.CharField(max_length=32)
    authorization_code = models.CharField(max_length=32)
    access_token = models.CharField(max_length=32)
    refresh_token = models.CharField(max_length=32)
