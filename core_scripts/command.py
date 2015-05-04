# -*- coding: utf-8 -*-
__author__ = 'reprintsevsv'
import json


class Command(object):
    CMD_SET = 'leg up'
    CMD_UNSET = 'leg down'

    def __init__(self, j):
        self.__dict__ = json.loads(j)
        return

    def __str__(self):
        return '%s %s' % (self.name, self.value)


class CommandInner(object):
    def __init__(self, cmd, leg, delay=0):
        self.cmd = cmd
        self.leg = leg
        self.delay = delay

    def __str__(self):
        return "%s %s %s" % (self.cmd, self.leg, self.delay)