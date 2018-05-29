from vehicle import Vehicle
import time

class SteeringCar(Vehicle):
    def setup(self):
        self.target_power = 0 # parameter (-100 .. 100)
        self.target_steering = 50 # parameter (0 .. 100)
        self.accel_power = 100 # parameter (0 .. 100)
        self.accel_steering = 100 # parameter (0 .. 100)
        self.min_power = 0 # parameter (0..100)
        self.max_power = 100 # parameter (0..100)
        self.min_steering = 65 # parameter (0..100)
        self.max_steering = 85 # parameter (0..100)
        self._current_power = 0 # private (-100 .. 100)
        self._current_steering = 50 # private (0 .. 100)
        self.add_handler('forward', self.forward)
        self.add_handler('back', self.back)
        self.add_handler('left', self.left)
        self.add_handler('right', self.right)
        self.add_handler('stop', self.brake)
        self.add_variable('power', self.set_moving_time)
        self.add_variable('steering', self.set_target_steering)
        self.add_variable('accel_power', self.set_accel_power)
        self.add_variable('accel_steering', self.set_accel_steering)
        self.add_variable('min_power', self.set_min_power)
        self.add_variable('max_power', self.set_max_power)
        self.add_variable('min_steering', self.set_min_steering)
        self.add_variable('max_steering', self.set_max_steering)

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

    def spin_once(self):
        self.update_power()
        self.update_steering()

    def forward(self):
        self.target_steering = 50
        self.target_power = 75

    def back(self):
        self.target_steering = 50
        self.target_power = -50

    def left(self):
        self.target_steering = 100

    def right(self):
        self.target_steering = 0

    def brake(self):
        self.target_power = 0

    def set_target_power(self, val):
        self.target_power = min(max(int(val),-100),100)

    def set_target_steering(self, val):
        self.target_steering = min(max(int(val),0),100)

    def set_accel_power(self, val):
        self.accel_power = min(max(int(val),0),100)

    def set_accel_steering(self, val):
        self.accel_steering = min(max(int(val),0),100)

    def set_min_power(self, val):
        self.min_power = min(max(int(val),0),100)

    def set_max_power(self, val):
        self.max_power = min(max(int(val),0),100)

    def set_min_steering(self, val):
        self.min_steering = min(max(int(val),0),100)

    def set_max_steering(self, val):
        self.max_steering = min(max(int(val),0),100)

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
