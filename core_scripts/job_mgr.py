import time

from core_scripts.job import Job

__author__ = 'bonecrusher'


for i in range(1, 2000):
    job = Job()
    print(i)
    job.init()
    job.execute()
    time.sleep(10)
