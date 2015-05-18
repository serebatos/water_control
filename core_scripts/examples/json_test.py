import json
from json import dumps, loads, JSONEncoder, JSONDecoder
import pickle
from core_scripts.command import CommandInner, Command

__author__ = 'bonecrusher'



data = {'message': 'hello world!', 'test': 123.4}
i_cmd = CommandInner(Command.CMD_SET,22,2)

print json.dumps(data)
