from django.db import models

# Create your models here.

class Coopon(models.Model):
    phone_number = models.CharField(max_length=300, null=True)
    number = models.CharField(max_length=100,default=0, unique=True)
    activate = models.BooleanField(default=False)

    def __str__(self):
        return self.number


class Coopon_icool(models.Model):
    phone = models.CharField(max_length=100, null=True)
    number = models.CharField(max_length=300, default=0, unique=True)
    activate = models.BooleanField(default=False)
    edittime = models.DateTimeField(auto_now=True)
    usetime = models.DateTimeField(null=True)

    def __str__(self):
        return self.pk