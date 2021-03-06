#!/usr/bin/env python
# author: Eiichiro Ito
# e-mail: e-itoh@ygu.ac.jp
# created: 2018/5/26
# License: MIT License
#
# Raspberry Pi Buggy
#  device --- GPIO Steering Car
from rsp_server.rsserver import RemoteSensorServer
from common.steeringcar import SteeringCar
from hardware.gpiosteering import GpioSteering
from hardware.ultrasonic import UltraSonic

if __name__ == '__main__':
    device = GpioSteering()
    server = RemoteSensorServer()
    robot = SteeringCar(device=device, server=server)
    robot.add_sensor('ultrasonic', UltraSonic())
    robot.spin()
