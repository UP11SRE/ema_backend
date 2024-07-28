   # file_manager/models.py
from django.db import models
from django.contrib.auth.models import User

class File(models.Model):
  name = models.CharField(max_length=255)
  size = models.BigIntegerField()
  owner = models.ForeignKey(User, related_name='owned_files', on_delete=models.CASCADE)
  shared_with = models.ManyToManyField(User, related_name='shared_files', blank=True)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  google_drive_id = models.CharField(max_length=255, unique=True)
  content_type = models.CharField(max_length=255, blank=True, null=True)

  def __str__(self):
      return self.name
