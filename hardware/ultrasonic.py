#!/usr/bin/env python
# author: Eiichiro Ito
# e-mail: e-itoh@ygu.ac.jp
# created: 2018/5/29
# License: MIT License
#
# Gpio Ultrasonic Sensor
#  HC-SR04 -- using WiringPi2 (GPIO-connected sensor).
import wiringpi as wp
import time
from threading import Thread, Event

TRIG=17
ECHO=27

GPIOMODE_IN=0
GPIOMODE_OUT=1
GPIOMODE_PWM=2

class UltraSonic(object):
    def __init__(self, force=False):
        if force:
            wp.wiringPiSetupGpio()
        wp.pinMode(TRIG, GPIOMODE_OUT)
        wp.pinMode(ECHO, GPIOMODE_IN)
        self.result = 0
        self.stop_event = Event()
        self.thread = Thread(target=self._thread)
        self.thread.daemon = True

    def start(self):
        self.thread.start()

    def stop(self):
        self.stop_event.set()
        self.thread.join()

    def distance(self):
        return self.result

    def values(self):
        return {'distance': self.result}

    def _thread(self):
        print("ultra sonic sensor thread start")
        while not self.stop_event.is_set():
            #print("step")
            ret = self._distance()
            if ret == 0:
                print("ultra sonic sensor timeout")
            else:
                #print("ret=%d" % ret)
                self.result = ret
            time.sleep(0.5)
        print("ultra sonic sensor thread end")

    def _distance(self):
        wp.digitalWrite(TRIG, 0)
        wp.delayMicroseconds(2)
        wp.digitalWrite(TRIG, 1)
        wp.delayMicroseconds(10)
        wp.digitalWrite(TRIG, 0);
        start = wp.micros()
        timeout = start + 1000000
        while wp.digitalRead(ECHO)==0 and start < timeout:
            start = wp.micros()
        if start > timeout:
            return 0
        end = wp.micros()
        while wp.digitalRead(ECHO)==1 and end < timeout:
            end = wp.micros()
        if end > timeout:
            return 0
        duration = end - start
        distance= duration*0.034/2;
        return distance

if __name__ == '__main__':
    u = UltraSonic(force=True)
    u.start()
    for x in range(10):
        d = u.distance()
        print("distance=%d" % d)
        time.sleep(1)
    u.stop()
