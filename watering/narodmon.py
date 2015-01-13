#!/usr/bin/env python
import glob
import time
import datetime
import socket



__author__ = 'bonecrusher'

# MAC
DEVICE_NAME = 'RaspberryPi'
DEVICE_MAC = '00:0f:13:30:0a:92'  # 00:0f:13:30:0a:92
DEVICE_LATITUDE = '56.075551'
DEVICE_LONGITUDE = '37.379672'
# Sensor id
# SENSOR_ID_2 = '28-00000609ea28'
SENSOR_ID_2 = '28-000006098521'
SENSOR_NAME = 'Street(DS18B20)'

# set up the location of the sensor in the system
device_folder = glob.glob('/sys/bus/w1/devices/28*')
device_file = []
if len(device_folder) > 0:
    device_file = [device_folder[0] + '/w1_slave', device_folder[1] + '/w1_slave']

dev_list = {}


def read_temp_raw():  # a function that grabs the raw temperature data from the sensor
    if len(device_file) > 0:
        f_1 = open(device_file[0], 'r')
        lines_1 = f_1.readlines()
        f_1.close()
        f_2 = open(device_file[1], 'r')
        lines_2 = f_2.readlines()
        f_2.close()
        return lines_1 + lines_2
    else:
        return ""


def read_temp():  # a function that checks that the connection was good and strips out the temperature
    lines = read_temp_raw()
    if len(lines) > 0:
        while lines[0].strip()[-3:] != 'YES' or lines[2].strip()[-3:] != 'YES':
            time.sleep(0.1)
            lines = read_temp_raw()
        equals_pos = lines[1].find('t='), lines[3].find('t=')
        temp = float(lines[1][equals_pos[0] + 2:]) / 1000, float(lines[3][equals_pos[1] + 2:]) / 1000
        dev_list[device_folder[0][(device_folder[0].rfind('/') + 1):]] = float(lines[1][equals_pos[0] + 2:]) / 1000
        dev_list[device_folder[1][(device_folder[1].rfind('/') + 1):]] = float(lines[3][equals_pos[1] + 2:]) / 1000
        return temp


def get_devices():
    # for dev in device_folder:
    # pos = dev.rfind('/') + 1
    # dev_list.append(dev[pos:])
    return dev_list


read_temp()
dev_list = get_devices()
second = dev_list[SENSOR_ID_2]
if second is not None:
    # create socket
    sock = socket.socket()

    try:
        # connect to basecamp
        sock.connect(('narodmon.ru', 8283))

        # writing single value of sensor 56.075551, 37.379672
        str = "#{}#{}#{}#{}\n#{}#{}#{}\n##".format(DEVICE_MAC, DEVICE_NAME, DEVICE_LATITUDE, DEVICE_LONGITUDE,
                                                   SENSOR_ID_2, second, SENSOR_NAME)
        sock.send(str)
        # writing multiple values of secsors
        # sock.send("#{}\n#{}#{}\n#{}#{}\n##".format(DEVICE_MAC, SENSOR_ID_1, sensor_value_1, SENSOR_ID_2, sensor_value_2))

        # get answer
        data = sock.recv(1024)
        # sock.close()
        print data
    except socket.error, e:
        print('ERROR! Exception {}'.format(e))