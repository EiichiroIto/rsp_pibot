from vehicle import Vehicle
import time

class TwoWheelsCar(Vehicle):
    def setup(self):
        self.moving_time = 1000 # parameter (ms)
        self.moving_power = 100 # parameter (-100..100)
        self.balance = 50 # parameter (0..100)
        self.turning_time = 300 # parameter (ms)
        self.turning_power = 100 # parameter (0..100)
        self._move_timeout = 0 # private
        self._current_left = 0 # private
        self._current_right = 0 # private
        self._target_left = 0 # private
        self._target_right = 0 # private
        self.add_handler('forward', self.forward)
        self.add_handler('back', self.back)
        self.add_handler('left', self.left)
        self.add_handler('right', self.right)
        self.add_handler('stop', self.brake)
        self.add_variable('moving_time', self.set_moving_time)
        self.add_variable('moving_power', self.set_moving_power)
        self.add_variable('balance', self.set_balance)
        self.add_variable('turning_time', self.set_turning_time)
        self.add_variable('turning_power', self.set_turning_power)

    def now_msec(self):
        return int(time.time()*1000)

    def motor(self, left, right):
        if self.device is None:
            return
        self.device.powerA(left)
        self.device.powerB(right)

    def new_current(self, current, target):
        return target

    def update_current(self):
        changed = False
        if self._current_left != self._target_left:
            changed = True
            self._current_left = self.new_current(self._current_left, self._target_left)
        if self._current_right != self._target_right:
            changed = True
            self._current_right = self.new_current(self._current_right, self._target_right)
        if changed:
            self.motor(self._current_left, self._current_right)

    def spin_once(self):
        if self._move_timeout > 0 and self.now_msec() > self._move_timeout:
            self.brake()
        self.update_current()

    def set_target(self, left, right):
        self._target_left = int(left)
        self._target_right = int(right)

    def forward(self):
        left = self.moving_power * min(self.balance, 50) / 50.0
        right = self.moving_power * min(100 - self.balance, 50) / 50.0
        self.set_target(left, right)
        self._move_timeout = self.now_msec() + self.moving_time

    def left(self):
        left = self.turning_power
        right = - self.turning_power
        self.set_target(left, right)
        self._move_timeout = self.now_msec() + self.turning_time

    def right(self):
        left = - self.turning_power
        right = self.turning_power
        self.set_target(left, right)
        self._move_timeout = self.now_msec() + self.turning_time

    def back(self):
        left = - (self.moving_power * min(self.balance, 50) / 50.0)
        right = - (self.moving_power * min(100 - self.balance, 50) / 50.0)
        self.set_target(left, right)
        self._move_timeout = self.now_msec() + self.moving_time

    def brake(self):
        self.set_target(0, 0)
        self._move_timeout = 0

    def set_moving_time(self, val):
        self.moving_time = int(val)

    def set_moving_power(self, val):
        self.moving_power = min(max(int(val),-100),100)

    def set_balance(self, val):
        self.balance = min(max(int(val),0),100)

    def set_turning_time(self, val):
        self.turning_time = int(val)

    def set_turning_power(self, val):
        self.turning_power = min(max(int(val),0),100)

if __name__ == '__main__':
    car = TwoWheelsCar(device=None, server=None)
    car.broadcast('forward')
