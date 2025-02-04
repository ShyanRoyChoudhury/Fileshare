from django.db import models
import uuid
import os
from django.utils.crypto import get_random_string
from django.utils import timezone
from enum import IntEnum

class PermissionTypes(IntEnum):
  """
    enum class for use in File Link permission model
  """
  Read = 1
  Write = 2
  
  @classmethod
  def choices(cls):
    return [(key.value, key.name) for key in cls]

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
    mfa_secret = models.CharField(max_length=16, blank=True, null=True)
    mfa_enabled = models.BooleanField(default=False)

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
    # salt = models.BinaryField(max_length=16, null=True, blank=True)  # 16 bytes standard for PBKDF2
    # iv = models.BinaryField(max_length=12, null=True, blank=True)    # 12 bytes for AES-GCM
    key = models.CharField(max_length=200, null=True, blank=True)


class FileDownloadLink(models.Model):
    id = models.AutoField(primary_key=True)
    token = models.CharField(max_length=64, unique=True, )
    created_at = models.DateTimeField(auto_now=True)
    expires_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)
    file = models.ForeignKey(Files, on_delete=models.CASCADE)
    permission = models.IntegerField(choices=PermissionTypes.choices(), default=PermissionTypes.Read)

    def generate_token(self):
        return get_random_string(length=64)
    
    def save(self, *args, **kwargs):
        if not self.token:
            self.token = self.generate_token()
        super().save(*args, **kwargs)

    def is_expired(self):
        return timezone.now() > self.expires_at
    
    def mark_as_used(self):
        self.is_used = True
        self.save()