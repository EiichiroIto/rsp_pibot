#!/usr/bin/env python
# author: Eiichiro Ito
# e-mail: e-itoh@ygu.ac.jp
# created: 2018/5/26
# License: MIT License
#
# Raspberry Pi Rover
#  motor -- using WiringPi2 (GPIO-connected, check following pin connections).
#  camera -- using takephoto script.
import wiringpi as wp

MOTOR_IN1A = 3 # WiringPi2 GPIO pin #
MOTOR_IN1B = 2 # WiringPi2 GPIO pin #
MOTOR_IN2A = 4 # WiringPi2 GPIO pin #
MOTOR_IN2B = 0 # WiringPi2 GPIO pin #

class GpioTwoWheels(object):
    def __init__(self):
        wp.wiringPiSetup()
        wp.softPwmCreate(MOTOR_IN1A,0,100)
        wp.softPwmCreate(MOTOR_IN1B,0,100)
        wp.softPwmCreate(MOTOR_IN2A,0,100)
        wp.softPwmCreate(MOTOR_IN2B,0,100)

    def powerA(self, power):
        v1 = int(power) if power > 0 else 0
        v2 = 0 if power > 0 else - int(power)
        wp.softPwmWrite(MOTOR_IN1A, v1)
        wp.softPwmWrite(MOTOR_IN1B, v2)

    def powerB(self, power):
        v1 = int(power) if power > 0 else 0
        v2 = 0 if power > 0 else - int(power)
        wp.softPwmWrite(MOTOR_IN2A, v1)
        wp.softPwmWrite(MOTOR_IN2B, v2)
