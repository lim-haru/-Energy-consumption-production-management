from django.db import models
from django.utils import timezone

class SessionHistory(models.Model):
    browser = models.CharField(max_length=20)
    ip = models.CharField(max_length=15)
    country = models.CharField(max_length=20)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.date.strftime('%Y/%m/%d - %H:%M')