# -*- coding: utf-8 -*-
# Обработчик команд для малины
# Логика:
# 1. получаем команду из сокета
# 2. десериализуем и кладем в очередь, которая обслуживается в отдельном потоке
# 3. Пока команды две - поднять ногу и опустить, соответственно, обрабатываем их поднимая или опуская ногу
# todo: , 2. Возвращать ответ в случае ошибки или невозможности, 3.
import logging

__author__ = 'Serebatos'
import json
import socket
import os

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
count = 0


def processCommand(q):
    while True:
        logger.debug('Looking for the next command')
        command = q.get()
        logger.info('%s Processing: %s, value: %s', time.time(), command.name, command.value)
        pin = int(command.value)
        if Command.CMD_SET == command.name:
            # GPIO.setup(pin, GPIO.OUT)
            # GPIO.output(pin, GPIO.HIGH)
            logger.info("Leg %s was set to HIGH OUT", command.value)
        elif Command.CMD_UNSET == command.name:
            # GPIO.setup(pin, GPIO.IN)
            logger.info("Leg %s was set to IN", command.value)

        q.task_done()


worker = Thread(target=processCommand, args=[command_queue])
worker.setDaemon(True)
worker.start()

# setup GPIO
# GPIO.setmode(GPIO.BOARD)
# GPIO.setwarnings(False)

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
server_address = ('localhost', 10000)
logger.info('Starting up on %s', server_address)
sock.bind(server_address)

# Listen for incoming connections
sock.listen(1)
i = 1

# Endless loop
while True:
    # Wait for a connection
    logger.info('Waiting for a connection')
    connection, client_address = sock.accept()

    try:
        logger.info('%s:connection from %s', i, client_address)

        # Receive the data in small chunks and retransmit it
        # while True:
        data = connection.recv(100).strip()
        logger.info('Received "%s"', data)
        if data:
            cmd = Command(data)
            logger.info("Command is '%s %s'", cmd.name, cmd.value)
            i += 1
            command_queue.put(cmd)
            # todo: Результат необходимо слать не бутафорский ОК, а реальную картину дел отражать..
            response = Result.get_leg_switch_ok()
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
