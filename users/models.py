from django.db import models

from core.models import TimeStamp

class User(TimeStamp):
    social_id = models.CharField(max_length=100)
    nickname = models.CharField(max_length=20)
    profile_image = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)

    class Meta:
        db_table = 'users'
