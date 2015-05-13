from threading import Thread
import time
import threading
from core_scripts.cmd_client import CommandSender
from core_scripts.cmd_processor import CommandProcessor
from core_scripts.command import Command, CommandInner
from core_scripts.result import Result
import unittest

__author__ = 'bonecrusher'


def thread(arg1, event):
    c = CommandProcessor()
    c.start(event,host='localhost', port=22000)


class CommandTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("Setup")
        cls.stop_event = threading.Event()
        cls.worker = Thread(target=thread, args=(1, cls.stop_event))
        cls.worker.setDaemon(True)
        cls.worker.start()

        cls.cs = CommandSender()
        cls.leg = 7
        cls.delay = 5

    def test_send_set(self):
        i_cmd = CommandInner(Command.CMD_SET, self.leg)
        result = CommandSender.send(i_cmd)
        self.assertIsNotNone(result, "Result is null")
        self.assertEqual(Command.CMD_SET, result.operation, 'Operation is wrong')
        self.assertEqual(str(self.leg), result.leg, 'Leg is wrong')
        self.assertEqual("1", result.value, 'Value is wrong')
        self.assertEqual(Result.OK, result.result, 'Result is wrong')

    def test_send_set_with_delay(self):
        i_cmd = CommandInner(Command.CMD_SET, self.leg, self.delay)
        result = CommandSender.send(i_cmd)
        self.assertIsNotNone(result, "Result is null")
        self.assertEqual(Command.CMD_SET, result.operation, 'Operation is wrong')
        self.assertEqual(str(self.leg), result.leg, 'Leg is wrong')
        self.assertEqual("0", result.value, 'Value is wrong')

        self.assertEqual(Result.OK, result.result, 'Result is wrong')
        # self.assertEqual(1, 1)

    @classmethod
    def tearDownClass(cls):
        print("Teardown")
        cls.stop_event.set()


if __name__ == '__main__':
    # unittest.main()
    suite = unittest.TestLoader().loadTestsFromTestCase(CommandTestCase)
    unittest.TextTestRunner(verbosity=2).run(suite)