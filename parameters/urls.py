from django.conf.urls import patterns, url
from parameters import views

urlpatterns = patterns('',
                       url(r"list/{0,1}$", views.ListParams.as_view(), name="list"),
                       url(r"view/(?P<id_par>[a-z0-9]+)/{0,1}$", views.param, name="view"),
                       url(r"create/{0,1}$", views.CreateParam.as_view(), name="create"),
                       url(r"edit/(?P<id_par>[a-z0-9]+)/{0,1}$", 
                           views.EditParam.as_view(),
                           name = "edit"
                       ))
                       
                       
    
