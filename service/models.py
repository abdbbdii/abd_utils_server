from django.db import models

class Settings(models.Model):
    google_credentials = models.TextField(default=None, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    password = models.TextField(default=None, null=True)
