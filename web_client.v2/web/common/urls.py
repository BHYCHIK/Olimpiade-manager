from django.conf.urls import patterns, include, url

urlpatterns = patterns('common.views',
    url(r'^$', 'index'),
)
