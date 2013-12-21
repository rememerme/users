from django.conf.urls import patterns, include, url

from rest import views

urlpatterns = patterns('',
    url(r'^/$', views.UsersListView.as_view()),
    url(r'^$', views.UsersListView.as_view())
)
