from django.db import models
from django.contrib.auth.models import User 

class TiqUserProfile(models.Model):
   user = models.ForeignKey(User, unique=True)
   session_id = models.CharField(max_length=200)
