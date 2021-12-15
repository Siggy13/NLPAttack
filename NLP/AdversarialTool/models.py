from django.db import models
from django.contrib.auth.models import User

class Attacks(models.Model):
    originalText = models.CharField(max_length=2000)
    AttackedText = models.CharField(max_length=2000)
    attackType = models.CharField(max_length=100, default="")
    User = models.ForeignKey(User, on_delete=models.CASCADE)