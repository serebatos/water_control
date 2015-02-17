# -*- coding: utf-8 -*-
import json
import time
import socket
import sys
from core_scripts.command import Command
from core_scripts.result import Result

__author__ = 'reprintsevsv'
from Queue import Queue
from threading import Thread
import time

command_queue = Queue()
count = 0


def processCommand(q):
    while True:
        print 'Looking for the next command\n'
        i = 2
        command = q.get()
        print('%s Processing: %s, value: %s' % (time.time(), command.name, command.value))

        # instead of really downloading the URL,
        # we just pretend and sleep
        print('sleep for %s' % i)
        time.sleep(i)
        q.task_done()


worker = Thread(target=processCommand, args=[command_queue])
worker.setDaemon(True)
worker.start()


# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
server_address = ('localhost', 10000)
print >> sys.stderr, 'starting up on %s port %s' % server_address
sock.bind(server_address)

# Listen for incoming connections
sock.listen(1)
i = 1
while True:
    # Wait for a connection
    print >> sys.stderr, 'waiting for a connection'
    connection, client_address = sock.accept()

    try:
        print >> sys.stderr, i, ':connection from', client_address

        # Receive the data in small chunks and retransmit it
        # while True:
        data = connection.recv(100).strip()
        print >> sys.stderr, 'received "%s"' % data
        # if data:
        # print >> sys.stderr, 'sending data back to the client'
        # connection.sendall(data)
        # else:
        # print >> sys.stderr, 'no more data from', client_address
        # break
        if data:
            cmd = Command(data)
            # print >> sys.stderr, cmd
            print "Command is ", cmd.name, cmd.value
            i += 1
            command_queue.put(cmd)
            response = Result.get_leg_switch_ok()
            connection.sendall(json.dumps(response))
        else:
            print >> sys.stderr, 'No data from client(', client_address, ').'

    finally:
        # Clean up the connection
        connection.close()

        # todo: instead of stub below start listening port for JSON message, then construct Command and put it in queue
        # for i in range(1, 10):
        # cmd = Command(Command.CMD_SET, i)
        # command_queue.put(cmd)
        # count += 1
        #
        #
        # time.sleep(20)
        # print '*** Main thread waiting'
        # command_queue.join()
        # print '*** Done'
        # print 'Sent = %s' % count

        # time.sleep(4)