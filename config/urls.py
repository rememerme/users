from django.conf.urls import patterns, include, url

#from django.contrib import admin
#admin.autodiscover()

urlpatterns = patterns('',
    url(r'^rest/v1/users/docs/', include('rest_framework_swagger.urls')),
    url(r'^rest/v1/users', include('rememerme.users.rest.urls'))
)
