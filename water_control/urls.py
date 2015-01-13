from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^blog/', include('blog.urls')),
    url(r'^', include('watering.urls')),
    # url(r'^watering/', include('watering.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
