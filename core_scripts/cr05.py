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

    def __init__(self):
        self.logger = logging.getLogger('valve')
        # who cares?))
        # GPIO.setwarnings(False)
        # setup our mode and pins
        GPIO.setmode(GPIO.BOARD)
        # set up GPIO output channel
        GPIO.setup(self.PIN_POWER_RELAY, GPIO.OUT)
        GPIO.setup(self.PIN_MOTOR_RELAY, GPIO.OUT)
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
        self.log("Opening valve")
        # Смотрим текущее состояние(есть траблы с точностью его определения)
        if not self.is_opened():
            self.log("Valve is not opened")
            # Добавляем обработчик сигнала полного открытия клапана, чтобы сразу после открытия выключить реле
            GPIO.add_event_detect(self.PIN_OPEN_SIGNAL, GPIO.FALLING, callback=self.on_open, bouncetime=600)
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
            self.log("Valve opened")
            # GPIO.remove_event_detect(self.PIN_OPEN_SIGNAL)
        else:
            self.log("Valve is already opened")

    def close(self):
        self.log("Closing valve")
        if not self.is_closed():
            self.log("Valve is not closed")
            GPIO.add_event_detect(self.PIN_CLOSE_SIGNAL, GPIO.FALLING, callback=self.on_close, bouncetime=600)
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
            self.log("Valve closed")
        else:
            self.log("Valve is already closed")
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
                "Valve is REALLY closed(channel %s)" % str(channel))
            if self.power == Valve.ON:
                time.sleep(0.5)
                self.power_off()

    # Обарботка сигнала "Кран открыт" - Почему-то срабатывает не всегда
    def on_open(self, channel):
        if int(GPIO.input(self.PIN_OPEN_SIGNAL)) == 0:
            self.log(
                "Valve is REALLY opened(channel %s)" % str(channel))
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
            res += 1
        if self.is_opened():
            res += 1
        return res

    def log(self, s, arg=None):
        if arg:
            s = s % arg
        self.logger.error(s)


if __name__ == '__main__':
    cr = Valve()
    print("Current state: %s" % cr.get_current_state())
    time.sleep(2)
    cr.open()
    # print("Set 16 to high")
    # GPIO.setmode(GPIO.BOARD)
    # GPIO.setup(16, GPIO.OUT)
    # GPIO.output(16, GPIO.HIGH)
    time.sleep(2)
    cr.close()



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