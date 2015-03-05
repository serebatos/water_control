# -*- coding: utf-8 -*-
import datetime
from core_scripts.cmd_client import CommandSender
from core_scripts.command import Command

__author__ = 'bonecrusher'

import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "water_control.settings")

import django
from watering.models import Branch, Status
import logging


django.setup()
print(django.VERSION)


class JobManager():
    # just created branches
    STATUS_NOT_INIT = 'not init'
    # branch is started and waiting for the running
    STATUS_PLANNED = 'plan'
    # branch is running
    STATUS_RUNNING = 'run'
    # branch is stopped even never running, but only started
    STATUS_STOPPED = 'stop'

    logger = logging.getLogger(__name__)
    planned_branches = []
    running_branches = []
    # интервал опоздания запуска, в течение которого после запланированного времени будет запущена ветка
    allowed_interval_min = 5
    allowed_interval = None

    # Инициализация, тут загружаем все, что понадобится для работы джоба
    def init(self):
        # self.logger.info('reading branches')
        planned = Status.objects.get(name=JobManager.STATUS_PLANNED)
        running = Status.objects.get(name=JobManager.STATUS_RUNNING)
        # Запланированные ветки, они ожидают запуска в работу
        self.planned_branches = Branch.objects.filter(status=planned.id)
        # Уже работающие ветки, ждут, когда их остановят и запланируют вновь
        self.running_branches = Branch.objects.filter(status=running.id)
        # формируем допустимый интервал
        self.allowed_interval = datetime.timedelta(minutes=self.allowed_interval_min)
        # self.logger.info('initialized')

    # сам джоб
    def execute(self):
        # self.logger.info('checking branches which are planned')
        branches_to_run = []
        branches_to_stop = []
        # ищем все, что запланировано и если пришло время - запускаем
        for planned_branch in self.planned_branches:
            t_curr = datetime.datetime.now()
            if planned_branch.t_start_plan:
                # наступило ли сейчас время запуска
                time_is_come = t_curr.time() > planned_branch.t_start_plan

                # проверям сколько времени прошло с момента, когда ветка должна была заработать
                # это нужно для того, например, если в 16:00 мы поливали 1 час, то т.к. у нас только время,
                # а не календарная дата, то в 18:00 ветка снова запустится, ибо 18 позднее 16, следовательно ай ай ай, как же
                # это мы пропустили запуск - надо запустить. А это не верно.
                # таким образом, если прослоупочили запуск более чем контрольный интервал(настраивается), то терпим до
                # следующего дня запуска. пока так возможно что-то можно еще придумать
                t_delta = datetime.datetime.combine(t_curr.date(), t_curr.time()) - datetime.datetime.combine(t_curr.date(),
                                                                                                              planned_branch.t_start_plan)
                # собственно, проверям, попадаем ли мы в разрешенный интервал опоздания запуска
                interval_is_allowed = t_delta < self.allowed_interval
                # если наступило время и мы в допустимом интервале, добавляем в список веток, подлежащих запуску
                if time_is_come and interval_is_allowed:
                    self.logger.info("%s is goin to start. Plan start time - (%s), Current time - (%s)",
                                     planned_branch.descr,
                                     planned_branch.t_start_plan, t_curr.time())
                    branches_to_run.append(planned_branch)
            else:
                self.logger.warning("Planned Branch %s has empty t_start_plan")

        # непосредственно запуск того, что отобрали
        self.run_branch(branches_to_run)

        # смотрим работающие ветки, если пришло время - останавливаем полив и ветку заново в статус Запланировано
        # , тут без допустимых интервалов все ок
        for running_branch in self.running_branches:
            t_curr = datetime.datetime.now()
            # пора останавливать?
            need_to_end = t_curr.time() > running_branch.t_end_plan

            # пришло время - в список на остановку
            if need_to_end:
                self.logger.info("%s is going to stop. Plan stop time - %s, Current tiem - %s", running_branch.descr,
                                 running_branch.t_end_plan, t_curr.time())
                branches_to_stop.append(running_branch)
        # останавливаем и переводим в статус снова запланирванных
        self.end_branch(branches_to_stop)

        # if not branches_to_run and not branches_to_stop:
        # self.logger.info("Nothing to stop/start!")

    # перевод статуса из PLANNED в RUNNING. Тут же надо дернуть ногу
    # todo: непосредственно дернуть ногой и тут и при остановке
    # todo: необходимо проверять, что нога поднялась при запуске и соотвественно опустилась при остановке полива!

    # todo: Нафиг убрать эти премудрости с плановыи и фактическим временем. сделать в лоб!!!! 17.02.15
    def run_branch(self, branch_list):
        # получаем новый статус - Работает
        status = Status.objects.get(name=JobManager.STATUS_RUNNING)
        for branch in branch_list:
            # проставляем новый статус
            branch.status = status
            # пишем фактическое время запуска
            branch.t_start_fact = datetime.datetime.now().time()
            t_curr = datetime.datetime.now()
            # рассчитываем плановое время остановки = план время запуска + длительность
            t_end_plan = datetime.datetime(t_curr.year, t_curr.month, t_curr.day, branch.t_start_plan.hour,
                                           branch.t_start_plan.minute) + datetime.timedelta(
                minutes=int(branch.duration))
            # сохраняем посчитанное
            branch.t_end_plan = t_end_plan
            branch.save()
            # Шлем команду на поднятие ноги
            res = CommandSender.send(Command.CMD_SET, branch.leg)
            # Поднять ногу!
            self.logger.info('Result: %s', res.result)
            if res.result == 'OK':
                self.logger.info('Command is completed successfully!')
            else:
                self.logger.warn('Error during processing command!')

            self.logger.info('%s is running now', branch.descr)
        if branch_list:
            self.logger.info('%s branches processed', len(branch_list))

    # running after completion must return to PLANNED state
    def end_branch(self, branch_list):
        # получаем новый статус - Заполнированно
        status = Status.objects.get(name=JobManager.STATUS_PLANNED)
        for branch in branch_list:
            # проставляем новый статус
            branch.status = status
            t_curr = datetime.datetime.now()
            # факт время остановки
            branch.t_end_fact = t_curr
            branch.save()
            # Опустить ногу!
            res = CommandSender.send(Command.CMD_UNSET, branch.leg)
            if res.result == 'OK':
                self.logger.info('Command is completed successfully!')
            else:
                self.logger.warn('Error during processing command!')

            self.logger.info('%s is stopped', branch.descr)

            # if branch_list:
            # self.logger.info('%s branches processed', len(branch_list))