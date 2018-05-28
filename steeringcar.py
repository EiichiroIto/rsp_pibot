import sys
from threading import Thread
import time

class SteeringCar(object):
    def __init__(self, device, server):
        self.device = device
        self.server = server
        self.target_power = 0 # parameter (-100 .. 100)
        self.target_steering = 50 # parameter (0 .. 100)
        self.accel_power = 10 # parameter (0 .. 100)
        self.accel_steering = 5 # parameter (0 .. 100)
        self.min_power = 0 # parameter (0..100)
        self.max_power = 100 # parameter (0..100)
        self.min_steering = 65 # parameter (0..100)
        self.max_steering = 85 # parameter (0..100)
        self.thread_interval = 200 # parameter (ms)
        self.camera_format = "jpg" # "jpg" or "gif" or "png"
        self._thread = None
        self._quit_loop = False
        self._current_power = 0 # private (-100 .. 100)
        self._current_steering = 50 # private (0 .. 100)
        self.device.setup()
        self.server.set_controller(self)

    def start(self):
        if self._thread is not None:
            return
        self._thread = Thread(target=self.timer_thread)
        self._thread.daemon = False #True
        self._thread.start()

    def stop(self):
        self._thread = None
        time.sleep(self.thread_interval/1000.0)
        self._quit_loop = True

    def power(self, value):
        v = int((self.max_power - self.min_power) / 100.0 * abs(value)) + self.min_power
        v = v if value > 0 else -v
        self.device.power(v)

    def steering(self, value):
        v = int((self.max_steering - self.min_steering) / 100.0 * value)+ self.min_steering
        self.device.steering(v)

    def update_power(self):
        diff = abs(self.target_power - self._current_power)
        if diff == 0:
            return
        if diff > self.accel_power:
            diff = self.accel_power
        if self.target_power > self._current_power:
            self._current_power = self._current_power + diff
        else:
            self._current_power = self._current_power - diff
        self.power(self._current_power)

    def update_steering(self):
        diff = abs(self.target_steering - self._current_steering)
        if diff == 0:
            return
        if diff > self.accel_steering:
            diff = self.accel_steering
        if self.target_steering > self._current_steering:
            self._current_steering = self._current_steering + diff
        else:
            self._current_steering = self._current_steering - diff
        self.steering(self._current_steering)

    def timer_thread(self):
        while self._thread is not None:
            self.update_power()
            self.update_steering()
            #self.updateSensors()
            #self.sendSensors()
            time.sleep(self.thread_interval/1000.0)

    def sensor_update(self, dic):
        for k in dic:
            key = k.encode('utf-8').lower()
            if type(dic[k]) is unicode:
                val = dic[k].encode('utf-8')
            else:
                val = str(dic[k])
            self.set_variable(key, val)

    def broadcast(self, m):
        message = m.encode('utf-8').replace(' ','').lower()
        if message == 'forward':
            self.target_steering = 50
            self.target_power = 75
        elif message == 'back':
            self.target_steering = 50
            self.target_power = -50
        elif message == 'left':
            self.target_steering = 100
        elif message == 'right':
            self.target_steering = 0
        elif message == 'stop':
            self.target_power = 0
        elif message == 'quit':
            self.stop()
            quit()
        else:
            print("broadcast(%s)" % message)

    def set_variable(self, _key, val):
        key = _key.replace(' ','').lower()
        if key == 'power':
            self.target_power = min(max(int(val),-100),100)
        elif key == 'steering':
            self.target_steering = min(max(int(val),0),100)
        elif key == 'accel_power':
            self.accel_power = min(max(int(val),0),100)
        elif key == 'accel_steering':
            self.accel_steering = min(max(int(val),0),100)
        elif key == 'min_power':
            self.min_power = min(max(int(val),0),100)
        elif key == 'max_power':
            self.max_power = min(max(int(val),0),100)
        elif key == 'min_steering':
            self.min_steering = min(max(int(val),0),100)
        elif key == 'max_steering':
            self.max_steering = min(max(int(val),0),100)
        elif key == 'thread_interval':
            self.thread_interval = min(max(int(val),0),100)
        elif key == 'camera_format':
            if val == 'jpg' or val == 'gif' or val == 'png':
                self.camera_format = val
        else:
            print("set_variable(%s, %s)" % (key, str(val)))

    def spin(self):
        try:
            self.start()
            if self.server is not None:
                self.server.start()
            while not self._quit_loop:
		time.sleep(1)
        finally:
            if self.server is not None:
                self.server.stop()
            self.stop()

class TestDevice(object):
    def setup(self):
        pass

    def power(self, val):
        print("power=%d" % val)

    def steering(self, val):
        print("steering=%d" % val)
            
if __name__ == '__main__':
    from rsp_server.rsserver import RemoteSensorServer
    device = TestDevice()
    server = RemoteSensorServer()
    c = SteeringCar(device=device, server=server)
    try:
        c.start()
        for x in range(20):
            print("sec=%d" % x)
            if x == 0:
                c.broadcast('forward')
            elif x == 3:
                c.broadcast('right')
            elif x == 6:
                c.sensor_update({'accel_steering': 5})
                c.broadcast('right')
            elif x == 9:
                c.broadcast('left')
            elif x == 14:
                c.broadcast('back')
            elif x == 18:
                c.broadcast('stop')
            time.sleep(1)
    finally:
        c.stop()
