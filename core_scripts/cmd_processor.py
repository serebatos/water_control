# -*- coding: utf-8 -*-
# Обработчик команд для малины
# Логика:
# 1. получаем команду из сокета
# 2. десериализуем и кладем в очередь, которая обслуживается в отдельном потоке
# 3. Пока команды две - поднять ногу и опустить, соответственно, обрабатываем их поднимая или опуская ногу
# todo: , 2. Возвращать ответ в случае ошибки или невозможности, 3.
import logging
import threading
import sys
from types import NoneType
from cr05 import Valve

__author__ = 'Serebatos'
import json
import socket
import os

sys.path.insert(0,'/home/pi/dev/remote/water_control/')
sys.path.append('/home/pi/dev/remote/')


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "water_control.settings")
import django
import logging


django.setup()
# import RPi.GPIO as GPIO

from command import Command
from result import Result

from Queue import Queue
from threading import Thread
import time

logger = logging.getLogger('cmd_processor')
command_queue = Queue()
response_queue = Queue()
count = 0
v = Valve()

def processCommand(q):
    while True:
        logger.debug('Looking for the next command')
        command = q.get()
        logger.info('%s Processing: %s, value: %s', time.time(), command.cmd, command.value)
        pin = int(command.value)
        f_set = 1
        f_uset = 0
        if Command.CMD_SET == command.cmd:
            # GPIO.setup(pin, GPIO.OUT)
            # GPIO.output(pin, GPIO.HIGH)
            v.start_watering(pin)
            logger.info("Leg %s was set to HIGH OUT", command.value)
            result = Result.get_leg_switch_ok(command.cmd, pin, f_set)
        elif Command.CMD_UNSET == command.cmd:
            # GPIO.setup(pin, GPIO.IN)
            v.stop_watering(pin)
            logger.info("Leg %s was set to LOW OUT", command.value)
            result = Result.get_leg_switch_ok(command.cmd, pin, f_uset)

        if 'delay' in command.__dict__:
            time.sleep(int(command.delay))
            if Command.CMD_SET == command.cmd:
                logger.info("Returning leg %s to LOW OUT", command.value)
                result = Result.get_leg_switch_ok(command.cmd, pin, f_uset)
            elif Command.CMD_UNSET == command.cmd:
                logger.info("Returning leg %s to HIGH OUT", command.value)
                result = Result.get_leg_switch_ok(command.cmd, pin, f_set)

        response_queue.put(result)
        q.task_done()


class CommandProcessor:
    worker = Thread(target=processCommand, name="CommandProcessorD", args=[command_queue])
    worker.setDaemon(True)
    worker.start()


    # setup GPIO
    # GPIO.setmode(GPIO.BOARD)
    # GPIO.setwarnings(False)

    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


    def initialize(self, host, port):
        # Bind the socket to the port
        server_address = (host, port)
        logger.info('Starting up on %s', server_address)
        self.sock.bind(server_address)
        # Liten for incoming connections
        self.sock.listen(1)

    def serve(self, stop_event):
        i = 1
        # Endless loop
        while (not stop_event.is_set()):
            # Wait for a connection
            logger.info('Waiting for a connection')
            connection, client_address = self.sock.accept()

            try:
                logger.info('%s:connection from %s', i, client_address)

                # Receive the data in small chunks and retransmit it
                # while True:
                data = connection.recv(100).strip()
                logger.info('Received "%s"', data)
                if data:
                    cmd = Command(data)
                    logger.info("Command is '%s %s'", cmd.cmd, cmd.value)
                    i += 1
                    command_queue.put(cmd)
                    response = response_queue.get()
                    connection.sendall(json.dumps(response))
                else:
                    logger.warn('No data from client(%s).', client_address)

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
        logger.info("Shutting down")

    def start(self, stop_event, host='localhost', port=10000):
        threading.currentThread().name = "CommandProcessor"
        self.initialize(host, port)
        if not stop_event:
            stop_event = threading.Event()
        self.serve(stop_event)


if __name__ == '__main__':
    cp = CommandProcessor()
    cp.start(threading.Event())