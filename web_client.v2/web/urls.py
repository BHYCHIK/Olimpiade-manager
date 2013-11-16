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
    url(r'^add_school$', 'common.views.add_school'),
    url(r'^schools$', 'common.views.get_schools'),
    url(r'^add_city_type$', 'common.views.add_city_type'),
    url(r'^add_city$', 'common.views.add_city'),
    url(r'^city_types$', 'common.views.city_types'),
    url(r'^cities$', 'common.views.cities'),
    url(r'^add_criteria_title$', 'common.views.add_criteria_title'),
    url(r'^criteria_titles$', 'common.views.criteria_titles'),
    url(r'^competitions$', 'common.views.competitions'),
    url(r'^start_competition$', 'common.views.start_competition'),
    url(r'^bad_login$', 'common.views.bad_login'),
    url(r'^add_role$', 'common.views.add_role'),
    url(r'^add_work$', 'common.views.add_work'),
    url(r'^add_score$', 'common.views.add_score'),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
