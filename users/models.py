from django.db import models

class User(models.Model):
    name = models.CharField(max_length=100)
# Create your models here.


class Subscriber(models.Model):
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)