from django.conf.urls.defaults import *
from settings import PATH_TO_THIS_MODULE

urlpatterns = patterns(PATH_TO_THIS_MODULE + '.views',
   (r'login', 'login'),
   (r'logout', 'logout'),
   (r'password_change', 'password_change'),
   (r'password_change_done', 'password_change_done'),
   (r'', 'login')
)