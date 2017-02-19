from django.db import models

# Create your models here.

class Token(models.Model):
  token = models.CharField(max_length=64)
  ts    = models.BigIntegerField()

  class Meta:
    app_label = 'api'

