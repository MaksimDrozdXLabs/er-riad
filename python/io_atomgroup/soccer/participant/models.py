from django.db import models

# Create your models here.

class Participant(models.Model):
    name = models.CharField(max_length=256)
    score = models.IntegerField()
    updated = models.DateTimeField(auto_now_add=True)
    created = models.DateTimeField(auto_now_add=True)
