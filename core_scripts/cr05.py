# -*- coding: utf-8 -*-
__author__ = 'bonecrusher'
import RPi.GPIO as GPIO
import time
import logging
import sys

FORMAT = '%(asctime)-15s %(message)s'
LOG_FILENAME = 'example.log'
logging.basicConfig(level=logging.DEBUG, format=FORMAT)


class Valve():
    ON = 'ON'
    OFF = 'OFF'
    # P4
    PIN_POWER_RELAY = 16

    # P5
    PIN_MOTOR_RELAY = 18

    # P3
    PIN_OPEN_SIGNAL = 15
    # P2
    PIN_CLOSE_SIGNAL = 13

    RELAY_SWITCH_TIME = 0.1

    # time to open\close, sec
    open_time = 5

    PIN_VALVE_REAR = 12
    PIN_VALVE_LEFT = 11
    PIN_VALVE_RIGHT = 22

    def __init__(self):
        self.logger = logging.getLogger('valve')
        # who cares?))
        GPIO.setwarnings(False)
        # setup our mode and pins
        GPIO.setmode(GPIO.BOARD)
        # set up GPIO output channel
        GPIO.setup(self.PIN_POWER_RELAY, GPIO.OUT)
        self.set_low(self.PIN_POWER_RELAY)
        GPIO.setup(self.PIN_MOTOR_RELAY, GPIO.OUT)
        self.set_low(self.PIN_MOTOR_RELAY)
        GPIO.setup(self.PIN_VALVE_REAR, GPIO.OUT)
        self.set_low(self.PIN_VALVE_REAR)
        GPIO.setup(self.PIN_VALVE_LEFT, GPIO.OUT)
        self.set_low(self.PIN_VALVE_LEFT)
        GPIO.setup(self.PIN_VALVE_RIGHT, GPIO.OUT)
        self.set_low(self.PIN_VALVE_RIGHT)
        GPIO.setup(self.PIN_OPEN_SIGNAL, GPIO.IN)
        GPIO.setup(self.PIN_CLOSE_SIGNAL, GPIO.IN)

        self.power = None


    def set_high(self, pin):
        GPIO.output(pin, GPIO.LOW)
        self.log("Set %s to HIGH", pin)
        pass

    def set_low(self, pin):
        GPIO.output(pin, GPIO.HIGH)
        self.log("Set %s to LOW", pin)
        pass

    def get_state(self):
        pass

    def open(self):
        self.log("Opening Hydrant")
        # Смотрим текущее состояние(есть траблы с точностью его определения)
        # if not self.is_opened():
        self.log("Hydrant is not opened")
        # Добавляем обработчик сигнала полного открытия клапана, чтобы сразу после открытия выключить реле
        # GPIO.add_event_detect(self.PIN_OPEN_SIGNAL, GPIO.FALLING, callback=self.on_open, bouncetime=600)
        # Сначала переключаем управляющее реле электромотора в режим ОТКРЫТИЯ
        self.set_low(self.PIN_MOTOR_RELAY)
        # даем релюшкам время для переключения
        time.sleep(Valve.RELAY_SWITCH_TIME)
        # включаем электромотор
        self.power_on()
        # работаем сколько нужно для полного открытия клапана плюс запас
        time.sleep(self.open_time)
        # Проверяем, было ли отключено питание по сигналу, нет - отключаем сами
        self.checked_power_off()
        self.log("Hydrant opened")
        # GPIO.remove_event_detect(self.PIN_OPEN_SIGNAL)
        # else:
        # self.log("Valve is already opened")

    def close(self):
        self.log("Closing Hydrant")
        # if not self.is_closed():
        self.log("Hydrant is not closed")
        # GPIO.add_event_detect(self.PIN_CLOSE_SIGNAL, GPIO.FALLING, callback=self.on_close, bouncetime=600)
        # Сначала переключаем управляющее реле электромотора в режим ЗАКРЫТИЯ
        self.set_high(self.PIN_MOTOR_RELAY)
        # даем релюшкам время для переключения
        time.sleep(Valve.RELAY_SWITCH_TIME)
        # подаем напругу через реле питания
        self.power_on()
        # работаем сколько нужно для полного закрытия клапана плюс запас
        time.sleep(self.open_time)
        # Проверяем, было ли отключено питание по сигналу, нет - отключаем сами
        self.checked_power_off()
        self.set_low(Valve.PIN_MOTOR_RELAY)
        self.log("Hydrant closed")
        # else:
        # self.log("Valve is already closed")
        # GPIO.remove_event_detect(self.PIN_CLOSE_SIGNAL)

    def power_on(self):
        self.log("Power on")
        self.set_high(self.PIN_POWER_RELAY)
        self.power = Valve.ON
        pass

    def power_off(self):
        self.log("Power off")
        self.set_low(self.PIN_POWER_RELAY)
        self.power = Valve.OFF

    # Выключение питания с проверкой "А не было ли оно уже выключено"
    def checked_power_off(self):
        if self.power == Valve.ON:
            self.power_off()

    # Включение питания с проверкой "А не было ли оно уже включено"
    def checked_power_on(self):
        if self.power == Valve.OFF:
            self.power_on()


    # Обарботка сигнала "Кран закрыт" - Почему-то срабатывает не всегда
    def on_close(self, channel):
        if int(GPIO.input(self.PIN_CLOSE_SIGNAL)) == 0:
            self.log(
                "Hydrant is REALLY closed(channel %s)" % str(channel))
            if self.power == Valve.ON:
                time.sleep(0.5)
                self.power_off()

    # Обарботка сигнала "Кран открыт" - Почему-то срабатывает не всегда
    def on_open(self, channel):
        if int(GPIO.input(self.PIN_OPEN_SIGNAL)) == 0:
            self.log(
                "Hydrant is REALLY opened(channel %s)" % str(channel))
            if self.power == Valve.ON:
                time.sleep(0.5)
                self.power_off()

    def is_opened(self):
        return int(GPIO.input(self.PIN_OPEN_SIGNAL)) == 0

    def is_closed(self):
        return int(GPIO.input(self.PIN_CLOSE_SIGNAL)) == 0

    def get_current_state(self):
        res = 0
        if self.is_closed():
            res += 2
        if self.is_opened():
            res += 1
        return res

    def log(self, s, arg=None):
        if arg:
            s = s % arg
        self.logger.error(s)

    def start_watering(self, leg):
        print("Open valve")
        self.set_high(leg)
        if not self.get_current_state() == 1:
            print("Open hydrant")
            self.open()

    def stop_watering(self, leg):
        if not self.get_current_state() == 2:
            print("Close hydrant")
            self.close()
        print("Close valve")
        self.set_low(leg)


if __name__ == '__main__':
    cr = Valve()

    if len(sys.argv) > 1:
        command = sys.argv[1]
        if len(sys.argv) > 2:
            area = sys.argv[2]
        print("Current state: %s" % cr.get_current_state())
        if command == "open":
            cr.open()
        elif command == "close":
            cr.close()
        elif command == "state":
            if cr.get_current_state() == 2:
                print("Hydrant is closed")
            elif cr.get_current_state() == 1:
                print("Hydrant is opened")
            elif cr.get_current_state() == 3:
                print("Hydrant is strange state...")

        elif command == "rear start":
            print("Open hydrant")
            cr.open()
            print("Open valve")
            cr.set_high(cr.PIN_VALVE_REAR)
        elif command == "rear stop":
            print("Close valve")
            cr.set_low(cr.PIN_VALVE_REAR)
            print("Close hydrant")
            cr.close()

        elif command == "left start":
            if not cr.get_current_state() == 1:
                print("Open hydrant")
                cr.open()
            print("Open valve")
            cr.set_high(cr.PIN_VALVE_LEFT)
        elif command == "left stop":
            print("Close valve")
            cr.set_low(cr.PIN_VALVE_LEFT)
            if not cr.get_current_state() == 2:
                print("Close hydrant")
                cr.close()



        else:
            print("Usage:todo")
    else:
        print("Usage:todo")
        # time.sleep(2)
        # cr.open()
        # print("Set 16 to high")
        # GPIO.setmode(GPIO.BOARD)
        # GPIO.setup(16, GPIO.OUT)
        # GPIO.output(16, GPIO.HIGH)
        # time.sleep(5)
        # cr.close()
        # GPIO.cleanup(Valve.PIN_POWER_RELAY)
        # GPIO.cleanup(Valve.PIN_CLOSE_SIGNAL)
        # GPIO.cleanup(Valve.PIN_MOTOR_RELAY)
        # GPIO.cleanup(Valve.PIN_OPEN_SIGNAL)




        # to use Raspberry Pi board pin numbers
        # pin = 16
        # delay = 2
        # print 'Delay is:', delay
        # GPIO.setmode(GPIO.BOARD)
        # # set up GPIO output channel
        # GPIO.setup(pin, GPIO.OUT)
        # # blink GPIO17 50 times
        # for i in range(0, 20):
        # blink(pin, delay, cr)
        # GPIO.cleanup(pin)