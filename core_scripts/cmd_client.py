import json
from core_scripts.command import Command
from core_scripts.result import Result

__author__ = 'bonecrusher'
import socket
import sys


# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('localhost', 10000)
print >> sys.stderr, 'connecting to %s port %s' % server_address
sock.connect(server_address)

try:

    # Send data
    j = '{"name":"' + Command.CMD_SET + '", "value": "1"}'
    print >> sys.stderr, 'sending (%s)' % j
    # sock.sendall(json.dumps(j))
    sock.sendall(j)

    # Look for the response
    amount_received = 0

    data = sock.recv(100).strip()
    print >> sys.stderr, "Raw data:", data
    response = json.loads(data)
    print >> sys.stderr, "1 Json loads: ", response
    response = json.loads(data)
    print >> sys.stderr, "2 Json loads: ", response
    amount_received += len(response)
    print >> sys.stderr, "Response length: ", amount_received

    res = Result(response)
    print >> sys.stderr, 'received "%s is %s"' % (res.operation, res.result)

finally:
    print >> sys.stderr, 'closing socket'
    sock.close()