# -*- coding: utf-8 -*-
__author__ = 'reprintsevsv'
import json


class Command(object):
    CMD_SET = 'leg up'
    CMD_UNSET = 'leg down'

    def  __init__(self, j):
        self.__dict__ = json.loads(j)
        return

    def __str__(self):
        return '%s %s', (self.name, self.value)
