from django.conf.urls.defaults import *
import settings

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
   (r'^user/', include('dfs_contact_web_lookup.tiq_login.urls')),
   (r'^contacts/', include('dfs_contact_web_lookup.contacts.urls')),
   (r'', 'tiq_login.views.login'),
)


if settings.DEBUG:
    urlpatterns += patterns('',
      (r'^site_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '/Users/mlmiller/django-projects/dfs_contact_web_lookup/site_media/'}),
    )
