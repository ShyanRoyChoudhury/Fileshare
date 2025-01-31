from django.db import models
import uuid
import os
# Create your models here.

def generateUID():
    return str(uuid.uuid4())

class User(models.Model):
    id = models.AutoField(primary_key=True)
    uid = models.CharField(max_length=50, unique=True, default=generateUID)
    name = models.CharField(max_length=80, null=True)
    created_at = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)
    email = models.EmailField(unique=True, max_length=50)
    number = models.CharField(unique=True, max_length=13, null=True)

    def __str__(self):
        return self.email

def get_upload_path(instance, fileName):
    return os.path.join(str(instance.user.uid), fileName)


class Files(models.Model):
    id = models.AutoField(primary_key=True)
    uid = models.CharField(max_length=50, unique=True, default=uuid.uuid4)
    file = models.FileField(upload_to=get_upload_path)
    name = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)