from django.conf import settings
from django.contrib.auth.models import User, check_password
from models import TiqUserProfile
from tiqLibraries.tiqErrors.tiqError import TiqError, TiqPasswordExpiredError
from tiq_login import getSessionRpcClient

class TiqLoginBackend:
   """
   """
   def authenticate(self, username=None, password=None):

      try:
         sessionRpcClient = getSessionRpcClient() 
         loginResult = sessionRpcClient.login(username, password)
      except TiqError, e:
         if (e.message == "Security Error: Password Expired."):
            raise TiqPasswordExpiredError, e.message
         return None

      if (loginResult['login'] != 'success'):
         print "bad login"
         return None
         
      try:
         user = User.objects.get(username=username)
        
      except User.DoesNotExist:
         user = User(username=username, password='')
         user.set_unusable_password()
         user.is_staff = True
         user.is_superuser = True
         user.sessionId = "DFS SESSION ID STRING"
         user.save()
         
         profile = TiqUserProfile.objects.create(user=user)

      else:
         profile = user.get_profile()
         
      profile.session_id = sessionRpcClient.sessionId
      print sessionRpcClient.sessionId
      profile.save()

      return user


   def get_user(self, user_id):
      try:
         return User.objects.get(pk=user_id)
      except User.DoesNotExist:
         return None
