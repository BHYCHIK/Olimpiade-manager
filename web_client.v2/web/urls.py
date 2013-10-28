from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.conf import settings

import settings
from django.conf.urls.static import static

urlpatterns = patterns('',
    url(r'^$', include('common.urls')),
    url(r'^register_person$', 'common.views.register_person'),
    url(r'^register_account$', 'common.views.register_account'),
    url(r'^thanks$', 'common.views.thanks'),
    url(r'^login$', 'common.views.account_login'),
    url(r'^logout$', 'common.views.account_logout'),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
