from django.conf.urls import patterns, url
from watering.views.temp_view import TempDeviceDetail
from watering.views.watering_view import WateringMain, BranchDetail, CommandView, BranchUpdate

urlpatterns = patterns('',
                       url(r'^$', WateringMain.as_view(), name='main'),
                       url(r'^branch/(?P<pk>\d+)/$', BranchDetail.as_view(), name='branch-detail'),
                       url(r'^branch/(?P<pk>\d+)/save$', BranchUpdate.as_view(), name='branch-upd'),
                       url(r'^branch/(?P<pk>\d+)/(?P<cmd>\w+)$', CommandView.as_view(), name='branch-cmd'),
                       url(r'^temp/(?P<pk>\d+)/$', TempDeviceDetail.as_view(), name='temp-detail'),
                       url(r'^temp/(?P<pk>\d+)/save$', TempDeviceDetail.as_view(), name='temp-upd'),
)