from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from tastypie.api import Api
from admin.api.resources import NurseResource

v1_api = Api(api_name='v1')
v1_api.register(NurseResource())

urlpatterns = patterns('',
                       url(r'^params/', include('parameters.urls', namespace="params")),
                       url(r'^admin/', include('admin.urls', namespace="admin")),
                       url(r'^api/', include(v1_api.urls))
    # Examples:
    # url(r'^$', 'nurses.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    #url(r'^admin/', include(admin.site.urls)),
                       
)
