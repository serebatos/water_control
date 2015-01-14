import datetime

__author__ = 'bonecrusher'

import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "water_control.settings")

import django
from watering.models import Branch, Status
import logging


django.setup()
print(django.VERSION)


class Job():
    # just created branches
    STATUS_NOT_INIT = 'not init'
    # branch is started and waiting for the running
    STATUS_PLANNED = 'plan'
    # branch is running
    STATUS_RUNNING = 'run'
    # branch is stopped even never running, but only started
    STATUS_STOPPED = 'stop'

    logger = logging.getLogger(__name__)
    started_branches = []
    running_branches = []

    def init(self):
        self.logger.info('reading branches')
        planned = Status.objects.get(name=Job.STATUS_PLANNED)
        running = Status.objects.get(name=Job.STATUS_RUNNING)
        self.started_branches = Branch.objects.filter(status=planned.id)
        self.running_branches = Branch.objects.filter(status=running.id)
        self.logger.info('initialized')

    def execute(self):
        self.logger.info('checking branches which are planned')
        branches_to_run = []
        branches_to_stop = []
        for started_branch in self.started_branches:
            t_curr = datetime.datetime.now()
            need_to_run = t_curr.time() > started_branch.t_start_plan
            self.logger.info("%s: current(%s)>branch_tstart(%s):%s", started_branch.descr, t_curr.time(),
                             started_branch.t_start_plan,
                             need_to_run)
            if need_to_run:
                branches_to_run.append(started_branch)
        self.run_branch(branches_to_run)

        self.logger.info('checking branches which are running')
        for running_branch in self.running_branches:
            t_curr = datetime.datetime.now()
            need_to_end = t_curr.time() > running_branch.t_end_plan
            self.logger.info("%s: current(%s)>branch.t_end_plan(%s):%s", running_branch.descr, t_curr.time(),
                             running_branch.t_end_plan,
                             need_to_end)
            if need_to_end:
                branches_to_stop.append(running_branch)
        self.end_branch(branches_to_stop)

        if not branches_to_run and not branches_to_stop:
            self.logger.info("Nothing to stop/start!")


    # from PLANNED state to RUNNING
    def run_branch(self, branch_list):
        status = Status.objects.get(name=Job.STATUS_RUNNING)
        for branch in branch_list:
            branch.status = status
            branch.t_start_fact = datetime.datetime.now().time()
            t_curr = datetime.datetime.now()
            t_end_plan = datetime.datetime(t_curr.year, t_curr.month, t_curr.day, branch.t_start_plan.hour,
                                           branch.t_start_plan.minute) + datetime.timedelta(
                minutes=int(branch.duration))
            branch.t_end_plan = t_end_plan
            branch.save()

            self.logger.info('%s is running now', branch.descr)
        if branch_list:
            self.logger.info('%s branches processed', len(branch_list))

    # running after completion must return to PLANNED state
    def end_branch(self, branch_list):
        status = Status.objects.get(name=Job.STATUS_PLANNED)
        for branch in branch_list:
            branch.status = status
            t_curr = datetime.datetime.now()
            branch.t_end_fact = t_curr
            branch.save()
            self.logger.info('%s is stopped', branch.descr)

        if branch_list:
            self.logger.info('%s branches processed', len(branch_list))