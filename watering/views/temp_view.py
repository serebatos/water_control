# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse, reverse_lazy
from django.utils import timezone
from django.views.generic import DetailView, FormView, UpdateView
from watering.models import Device

__author__ = 'bonecrusher'


# Получение детального представления датчика\устройства
class TempDeviceDetail(DetailView, UpdateView):

    model = Device
    # name of context variable which we use in template
    context_object_name = 'device'
    # name of template where details are displayed
    template_name = "watering/base_watering_tempdevice_details.html"
    # fields which we will change\edit
    fields = ['descr']

    # where we should be redirected after success operation
    success_url = reverse_lazy('main')

    def get_object(self):
        object = super(TempDeviceDetail, self).get_object()
        object.last_accessed = timezone.now()
        object.save()
        return object



