from django.db import models

class User(models.Model):

    username=models.CharField(max_length=20,unique=True)
    first_name=models.CharField(max_length=20)
    last_name=models.CharField(max_length=20)
    email=models.EmailField(unique=True)
    mobile=models.CharField(max_length=10,unique=True)
    password=models.CharField(max_length=30)

    def __str__(self):
        return self.name

    

class Timeconverter(models.Model):
    time = models.DateTimeField()
    timezone = models.CharField(max_length=50)
    

