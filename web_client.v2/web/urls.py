from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from django.conf import settings
admin.autodiscover()

import settings
from django.conf.urls.static import static

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', include('common.urls')),
    url(r'^register_person$', 'common.views.register_person'),
    url(r'^thanks$', 'common.views.thanks'),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
