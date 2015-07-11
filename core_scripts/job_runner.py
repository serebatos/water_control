import time
from job_manager import JobManager
__author__ = 'bonecrusher'

# for i in range(1, 2000):
while True:
    jm = JobManager()
    # print(i)
    jm.init()
    jm.execute()
    time.sleep(20)

