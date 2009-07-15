from django.db import models
from django.contrib.auth.models import User 

class CachedContacts(models.Model):
   cc_id = models.IntegerField(primary_key=True)
   user = models.ForeignKey(User)
   contact_id = models.IntegerField()
   contact_name = models.CharField(max_length=32)
   viewed =  models.IntegerField()
   last_viewed = models.DateTimeField(auto_now=True)