from django.conf.urls import patterns, url, include
from admin import views

urlpatterns = patterns('',
                       url("^nurses/{0,1}?",
                           views.ListNurses.as_view(),
                           name = "list_nurses"))
                           
