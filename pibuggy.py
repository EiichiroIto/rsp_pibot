#!/usr/bin/env python
# author: Eiichiro Ito
# e-mail: e-itoh@ygu.ac.jp
# created: 2018/5/26
# License: MIT License
#
# Raspberry Pi Buggy
#  steering motor -- using WiringPi2 (GPIO-connected mini servo motor).
#  drive motor -- using WiringPi2 (GPIO-connected DC motor).
from rsp_server.rsserver import RemoteSensorServer
from steeringcar import SteeringCar
import wiringpi as wp

MOTOR_OUTA=24
MOTOR_OUTB=23
MOTOR_PWM=25
STEERING_PORT=18

GPIOMODE_IN=0
GPIOMODE_OUT=1
GPIOMODE_PWM=2

class GpioSteering(object):
    def __init__(self):
        wp.wiringPiSetupGpio()
        wp.softPwmCreate(MOTOR_PWM, 0, 100)
        wp.pinMode(MOTOR_OUTA, GPIOMODE_OUT)
        wp.pinMode(MOTOR_OUTB, GPIOMODE_OUT)
        wp.pinMode(STEERING_PORT, GPIOMODE_PWM)
        wp.pwmSetMode(0)
        wp.pwmSetRange(1024)
        wp.pwmSetClock(375)

    def power(self, val):
        pwm = abs(val)
        (v1,v2) = (0,1) if val > 0 else (1,0)
        wp.digitalWrite(MOTOR_OUTA, v1)
        wp.digitalWrite(MOTOR_OUTB, v2)
        wp.softPwmWrite(MOTOR_PWM, pwm)

    def steering(self, val):
        wp.pwmWrite(STEERING_PORT, val)

if __name__ == '__main__':
    device = GpioSteering()
    server = RemoteSensorServer()
    robot = SteeringCar(device=device, server=server)
    robot.spin()
