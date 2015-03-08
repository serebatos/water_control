import time
import urllib2

__author__ = 'bonecrusher'

URL = "http://81.176.229.94"


def get_led_on():
    return "?cmd=setledon"


def get_led_off():
    return "?cmd=setledoff"


for i in range(0, 0):
    print(i % 2)
    if i % 2 == 0:
        print(URL + get_led_on())
        http_cmd = URL + get_led_on()
    else:
        print(URL + get_led_off())
        http_cmd = URL + get_led_off()

    req = urllib2.Request(http_cmd)
    response = urllib2.urlopen(req)
    the_page = response.read()
    time.sleep(1)


class User():
    def __init__(self, n):
        self.name = n

    def __str__(self):
        return self.name

    def __cmp__(self, other):
        return other.name == self.name


u1 = User('Test')

aList = [User('Test'), User('xyz'), User('zara'), 'abc']

print "Index for user: ", aList.index(u1)