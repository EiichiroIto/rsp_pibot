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

TRIG=17
ECHO=27

GPIOMODE_IN=0
GPIOMODE_OUT=1
GPIOMODE_PWM=2

start = 0
end = 0

class UltraSonic(object):
    def __init__(self, force=False):
        if force:
            wp.wiringPiSetupGpio()
        wp.pinMode(TRIG, GPIOMODE_OUT)
        wp.pinMode(ECHO, GPIOMODE_IN)

    def microSeconds(self):
        return int(time.time()*1000000)

    def distance(self):
        global start, end
        wp.digitalWrite(TRIG, 0)
        wp.delayMicroseconds(2)
        wp.digitalWrite(TRIG, 1)
        wp.delayMicroseconds(10)
        wp.digitalWrite(TRIG, 0);
        start = wp.micros()
        while wp.digitalRead(ECHO)==0:
            start = wp.micros()
        end = wp.micros()
        while wp.digitalRead(ECHO)==1:
            end = wp.micros()
        duration = end - start
        distance= duration*0.034/2;
        return distance

if __name__ == '__main__':
    u = UltraSonic(force=True)
    d = u.distance()
    print("distance=%d" % d)
    print("start=%d end=%d duration=%d" % (start, end, end-start))
