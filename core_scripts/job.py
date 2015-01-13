__author__ = 'bonecrusher'

import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "water_control.settings")

import django
from watering.models import Branch, Status
import logging
# START



django.setup()
print(django.VERSION)

branch_list = Branch.objects.all()

for branch in branch_list:
    print("Branch: ", branch)


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
    started_jobs = []

    def init(self):
        planned = Status.objects.get(name=Job.STATUS_PLANNED)
        self.started_jobs = Branch.objects.filter(status=planned.id)
        print repr(self.started_jobs)
        self.logger.info('initialized')

    def run(self):
        print('running')