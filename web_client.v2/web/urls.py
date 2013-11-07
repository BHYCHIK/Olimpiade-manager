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
    url(r'^about$', 'common.views.about'),
    url(r'^persons$', 'common.views.persons'),
    url(r'^login$', 'common.views.account_login'),
    url(r'^logout$', 'common.views.account_logout'),
    url(r'^add_school_type$', 'common.views.add_school_type'),
    url(r'^school_types$', 'common.views.school_types'),
    url(r'^add_city_type$', 'common.views.add_city_type'),
    url(r'^city_types$', 'common.views.city_types'),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
