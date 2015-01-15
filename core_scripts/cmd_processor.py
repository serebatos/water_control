from core_scripts.command import Command

__author__ = 'reprintsevsv'
from Queue import Queue
from threading import Thread
import time

command_queue = Queue()
count = 0


def processCommand(i, q):
    while True:
        print 'Looking for the next command\n'
        command = q.get()
        print('Processing: %s, valuse: %s' % (command.command_name, command.value))

        # instead of really downloading the URL,
        # we just pretend and sleep
        # time.sleep(i + 2)
        q.task_done()


worker = Thread(target=processCommand, args=(1, command_queue))
worker.setDaemon(True)
worker.start()

for i in range(1, 10):
    cmd = Command(Command.CMD_SET, i)
    command_queue.put(cmd)
    count += 1

print '*** Main thread waiting'
command_queue.join()
print '*** Done'

print 'Sent = %s' % count

# time.sleep(4)