from django.conf.urls import patterns, include, url

urlpatterns = patterns('rest.views',
    url(r'^$', 'index'),
)
