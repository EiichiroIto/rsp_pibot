#!/usr/bin/env python
# author: Eiichiro Ito
# e-mail: e-itoh@ygu.ac.jp
# created: 2018/5/26
# License: MIT License
#
# Raspberry Pi Rover
#  device -- GPIO Two Wheels Car
from rsp_server.rsserver import RemoteSensorServer
from twowheelscar import TwoWheelsCar
from robot.gpiotwowheels import GpioTwoWheels

if __name__ == '__main__':
    device = GpioTwoWheels()
    server = RemoteSensorServer()
    robot = TwoWheelsCar(device=device, server=server)
    robot.spin()
