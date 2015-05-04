# -*- coding: utf-8 -*-
__author__ = 'reprintsevsv'
import json


class Result(object):
    OK = 'OK'
    ERROR = 'ERROR'

    def __init__(self, j):
        self.__dict__ = json.loads(j)
        return

    def __str__(self):
        return "%s, %s, %s" % (self.operation, self.leg, self.result)

    @staticmethod
    def get_leg_switch_ok(cmd_name, leg, value):
        return '{"operation":"%s", "leg":"%s", "value":"%s", "result":"%s"}' % (
        cmd_name, str(leg), str(value), Result.OK)