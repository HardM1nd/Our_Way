from django.db import models 
from django.conf import settings

class CoreSetting(models.Model): 
    key = models.CharField(max_length=100, unique=True) 
    value = models.CharField(max_length=500)
    def __str__(self):
        return f'{self.key}: {self.value}'
