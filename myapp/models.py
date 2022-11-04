from django.db import models
from django.contrib.auth.models import User, AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils.timezone import datetime


# Create your models here.


class Device(models.Model):
    name = models.CharField(max_length=200)
    ipAdress = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)


class LatencyTest(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    result = models.CharField(max_length=200)
    dateTest = models.DateField(default=datetime.now, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
