# -*- coding: utf-8 -*-
from django import forms
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.views.generic import TemplateView, DetailView, RedirectView, FormView, UpdateView
from core_scripts.job import Job
from ..models import Branch, Status, Device
from ..temp_mon import *


__author__ = 'bonecrusher'


# Главная страница
class WateringMain(TemplateView):
    template_name = "watering/base_watering.html"


    def get_context_data(self, **kwargs):
        context = super(WateringMain, self).get_context_data(**kwargs)
        temperatures = read_temp()
        temp_dev_list = list(Device.objects.all())
        # Только при первом запуске(мудрить с init приложения не стал)
        if len(temp_dev_list) == 0:
            devices = get_devices()
            for d in devices:
                new_device = Device(name=d, descr=d)
                new_device.save()
            temp_dev_list = list(Device.objects.all())
        dd = []
        devices = get_devices()
        for dev, temp in devices.iteritems():
            dd.append({'device': dev, 'temp': temp})
            td = next(temp_dev for temp_dev in temp_dev_list if temp_dev.name == dev)
            if td:
                td.value = temp
        branches = Branch.objects.all()
        context['title'] = 'This is my app. It uses Django templates'
        context['result'] = branches
        context['temp_result'] = temp_dev_list

        return context


# Получение детального представления ветки
class BranchDetail(DetailView, UpdateView):
    model = Branch
    context_object_name = 'branch'
    template_name = "watering/base_watering_branch_details.html"
    fields = ['descr', 'duration']

    def get_object(self):
        object = super(BranchDetail, self).get_object()
        object.last_accessed = timezone.now()
        object.save()
        return object


class BranchForm(UpdateView):
    model = Branch
    fields = ['descr']
    template_name = 'watering/base_watering_branch_details.html'

    def form_valid(self, form):
        return super(BranchForm, self).form_valid(form)

    def get_object(self, queryset=None):
        return super(BranchForm, self).get_object(queryset)


# Команды для ветки
class CommandView(RedirectView):
    pattern_name = 'main'
    permanent = True

    def get_redirect_url(self, *args, **kwargs):
        branch = get_object_or_404(Branch, pk=kwargs['pk'])
        cmd = kwargs['cmd']
        stat = None
        if cmd == 'start':
            # todo: Replace pk=3
            stat = Status.objects.get(name=Job.STATUS_PLANNED)
        elif cmd == 'stop':
            # todo: Replace pk=4
            stat = Status.objects.get(name=Job.STATUS_STOPPED)
        if stat:
            branch.status = stat
            branch.save()
        return reverse(self.pattern_name)











