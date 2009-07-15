from django.conf.urls.defaults import *

urlpatterns = patterns('dfs_contact_web_lookup.contacts.views',
   (r'search', 'search'),
   (r'detail/(?P<contact_id>\d+)', 'detail'),
   (r'', 'search')
)