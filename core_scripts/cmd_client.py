import json
import logging
from result import Result

__author__ = 'bonecrusher'
import socket
import sys


class CommandSender():
    logger = logging.getLogger(__name__)

    @staticmethod
    def send(command, leg):
        # Create a TCP/IP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Connect the socket to the port where the server is listening
        server_address = ('localhost', 10000)
        CommandSender.logger.info('---------------------------------')
        CommandSender.logger.info('Connecting to %s', server_address)

        try:
            sock.connect(server_address)
            # Send data
            j = '{"name":"' + command + '", "value": "' + str(leg) + '"}'
            CommandSender.logger.info('Sending command (%s)', j)
            # sock.sendall(json.dumps(j))
            sock.sendall(j)

            # Look for the response
            amount_received = 0

            data = sock.recv(100).strip()
            CommandSender.logger.info("Got answer, raw data '%s'", data)
            response = json.loads(data)
            response = json.loads(data)
            amount_received += len(response)
            CommandSender.logger.info("Response '%s'", response)
            CommandSender.logger.info("Response length is %s", amount_received)

            res = Result(response)
            CommandSender.logger.info('Received "%s is %s"', res.operation, res.result)

        except Exception, err:
            CommandSender.logger.exception(str(err))
        finally:
            # print >> sys.stderr, 'closing socket'
            sock.close()
        return res

        # Create a TCP/IP socket
        # sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Connect the socket to the port where the server is listening
        # server_address = ('localhost', 10000)
        # print >> sys.stderr, 'connecting to %s port %s' % server_address
        # sock.connect(server_address)

        # try:

        # Send data
        # j = '{"name":"' + Command.CMD_SET + '", "value": "1"}'
        # print >> sys.stderr, 'sending (%s)' % j
        # sock.sendall(json.dumps(j))
        # sock.sendall(j)

        # Look for the response
        # amount_received = 0

        # data = sock.recv(100).strip()
        # print >> sys.stderr, "Raw data:", data
        # response = json.loads(data)
        # print >> sys.stderr, "1 Json loads: ", response
        # response = json.loads(data)
        # print >> sys.stderr, "2 Json loads: ", response
        # amount_received += len(response)
        # print >> sys.stderr, "Response length: ", amount_received
        #
        # res = Result(response)
        # print >> sys.stderr, 'received "%s is %s"' % (res.operation, res.result)
        #
        # finally:
        # print >> sys.stderr, 'closing socket'
        # sock.close()