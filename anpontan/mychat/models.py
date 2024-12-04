from django.db import models
from django.utils import timezone

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=50)
    group_id = models.CharField(max_length=10)
    islogin = models.BooleanField(default=False)

class Room(models.Model):
    name = models.TextField(null=False, blank=False)
