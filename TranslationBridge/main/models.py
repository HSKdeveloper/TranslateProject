from django.db import models

# Create your models here.

class Contact(models.Model):

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=False)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)