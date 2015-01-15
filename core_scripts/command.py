__author__ = 'reprintsevsv'


class Command(object):
    CMD_SET = 'leg up'
    CMD_UNSET = 'leg down'

    def __init__(self, cmd_name, value):
        self.command_name = cmd_name
        self.value = value
        # print 'New command:', cmd_name, value
        return

    def __str__(self):
        return self.command_name, ' - ', self.value

