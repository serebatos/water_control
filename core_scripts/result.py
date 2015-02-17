# -*- coding: utf-8 -*-
__author__ = 'reprintsevsv'
import json


class Result(object):

    def __init__(self, j):
        self.__dict__ = json.loads(j)
        return

    def __str__(self):
        return self.operation, ' - ', self.result

    @staticmethod
    def get_leg_switch_ok():
        return '{"operation":"leg switch", "result":"ok"}'