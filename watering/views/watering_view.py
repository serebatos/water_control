# -*- coding: utf-8 -*-
from django import forms
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.views.generic import TemplateView, DetailView, RedirectView, FormView, UpdateView
from core_scripts.cmd_client import CommandSender
from core_scripts.command import Command, CommandInner
from core_scripts.job_manager import JobManager
from ..models import Branch, Status, Device
from ..temp_mon import *
from datetime import datetime, date
from django.shortcuts import render
from watering.models import Maintanence_log, Maintanence


__author__ = 'bonecrusher'


# Главная страница
class WateringMain(TemplateView):
    template_name = "watering/base_watering.html"

    def get_time(self, str_time):
        try:
            res_time = datetime.strptime(str_time, "%H:%M").time()
        except:
            str_time = str_time.replace(".", "")
            res_time = datetime.strptime(str_time, "%I:%M %p").time()
        return res_time

    # Сохранение данных с главной страницы
    def post(self, request):
        post_data = request.POST
        key = "maintanence_inp"
        if post_data.has_key(key):
            value = post_data[key]
            if len(value):
                m_list = list(Maintanence.objects.filter(name=value))
                if not m_list or len(m_list) <= 0:
                    m = Maintanence(name=post_data[key])
                    m.save()
                else:
                    m = m_list[0]
                ml = Maintanence_log(maintanence=m, work_description='Test', last_accessed=datetime.now())
                ml.save()
        else:
            branches = Branch.objects.all()
            for b in branches:
                b_id = str(b.id)
                key = 't_start_plan_' + b_id
                if post_data.has_key(key):
                    t_start = post_data[key]

                key = 't_end_plan_' + b_id
                if post_data.has_key(key):
                    t_end = post_data[key]

                key = 'length_' + b_id
                if post_data.has_key(key):
                    len_from_form = post_data[key]

                b.t_start_plan = self.get_time(t_start)
                b.t_end_plan = self.get_time(t_end)
                delta = datetime.combine(date.today(), b.t_end_plan) - datetime.combine(date.today(), b.t_start_plan)
                l = delta.seconds / 60
                b.duration = l

                day = 'monday_' + b_id
                if post_data.has_key(day):
                    b.monday = True
                else:
                    b.monday = False

                day = 'tuesday_' + b_id
                if post_data.has_key(day):
                    b.tuesday = True
                else:
                    b.tuesday = False
                day = 'wednesday_' + b_id
                if post_data.has_key(day):
                    b.wednesday = True
                else:
                    b.wednesday = False
                day = 'thursday_' + b_id
                if post_data.has_key(day):
                    b.thursday = True
                else:
                    b.thursday = False
                day = 'friday_' + b_id
                if post_data.has_key(day):
                    b.friday = True
                else:
                    b.friday = False
                day = 'saturday_' + b_id
                if post_data.has_key(day):
                    b.saturday = True
                else:
                    b.saturday = False
                day = 'sunday_' + b_id
                if post_data.has_key(day):
                    b.sunday = True
                else:
                    b.sunday = False
                b.save()

        return render(request, self.template_name, self.get_context_data())


    def get_context_data(self, **kwargs):
        context = super(WateringMain, self).get_context_data(**kwargs)

        temperatures = read_temp()
        temp_dev_list = list(Device.objects.all())
        # Инициализация. Если в базе нет устройств
        if len(temp_dev_list) == 0:
            # то получем список подсоединенных устройств и пишем его в базу
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

        # Читаем полив
        branches = Branch.objects.all()

        # todo: last events for 3 month for example...
        maintanence_log = Maintanence_log.objects.all().order_by('-last_accessed')
        maintanence = Maintanence.objects.all()

        context['title'] = 'This is my app. It uses Django templates'
        context['result'] = branches
        context['temp_result'] = temp_dev_list
        context['maintanence'] = maintanence
        context['maintanence_log'] = maintanence_log

        return context


# Получение детального представления ветки
class BranchDetail(DetailView):
    model = Branch
    context_object_name = 'branch'
    template_name = "watering/base_watering_branch_details.html"


    def get_object(self):
        object = super(BranchDetail, self).get_object()
        last_accessed = object.last_accessed
        object.last_accessed = timezone.now()
        object.save()
        # Показываем предыдущее значение
        object.last_accessed = last_accessed
        return object


class BranchUpdate(RedirectView):
    pattern_name = 'main'
    permanent = True

    def get_redirect_url(self, *args, **kwargs):
        # ищем ветку
        branch = get_object_or_404(Branch, pk=kwargs['pk'])
        start_plan = self.request.POST['t_start_plan']
        try:
            branch.t_start_plan = datetime.strptime(start_plan, "%H:%M").time()
            branch.save()
        except:
            start_plan = start_plan.replace(".", "")
            branch.t_start_plan = datetime.strptime(start_plan, "%I:%M %p").time()
            branch.save()

        return reverse(self.pattern_name)


# Команды для ветки
class CommandView(RedirectView):
    pattern_name = 'main'
    permanent = True

    def get_redirect_url(self, *args, **kwargs):
        # ищем ветку
        branch = get_object_or_404(Branch, pk=kwargs['pk'])
        # по команде ищем статус из БД
        cmd = kwargs['cmd']
        stat = None

        if cmd == 'start':
            stat = Status.objects.get(name=JobManager.STATUS_PLANNED)
        elif cmd == 'stop':
            stat = Status.objects.get(name=JobManager.STATUS_STOPPED)
        elif cmd == 'on':
            stat = Status.objects.get(name=JobManager.STATUS_RUNNING)
            CommandSender.send(CommandInner(Command.CMD_SET, branch.leg))
        elif cmd == 'off':
            stat = Status.objects.get(name=JobManager.STATUS_STOPPED)
            CommandSender.send(CommandInner(Command.CMD_UNSET, branch.leg))

        if stat:
            branch.status = stat
            branch.save()
        return reverse(self.pattern_name)













