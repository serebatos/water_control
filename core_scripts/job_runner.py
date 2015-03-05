import time
from core_scripts.job_manager import JobManager
__author__ = 'bonecrusher'

for i in range(1, 2000):
    job = JobManager()
    print(i)
    job.init()
    job.execute()
    time.sleep(10)

