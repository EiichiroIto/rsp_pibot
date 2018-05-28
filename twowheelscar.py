from threading import Thread
import time

class TwoWheelsCar(object):
    def __init__(self, device, server):
        self.device = device
        self.moving_time = 1000 # parameter (ms)
        self.moving_power = 100 # parameter (-100..100)
        self.balance = 50 # parameter (0..100)
        self.turning_time = 300 # parameter (ms)
        self.turning_power = 100 # parameter (0..100)
        self.thread_interval = 200 # parameter (ms)
        self.camera_format = "jpg" # "jpg" or "gif" or "png"
        self._thread = None
        self._quit_loop = False
        self._move_timeout = 0 # private
        self._current_left = 0 # private
        self._current_right = 0 # private
        self._target_left = 0 # private
        self._target_right = 0 # private
        self.set_server(server)

    def set_server(self, server):
        self.server = server
        if self.server is not None:
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

    def timer_thread(self):
        while self._thread is not None:
            now = int(time.time()*1000)
            if self._move_timeout > 0 and now > self._move_timeout:
                self.brake()
            self.update_current()
            time.sleep(self.thread_interval/1000.0)

    def set_target(self, left, right):
        self._target_left = int(left)
        self._target_right = int(right)

    def brake(self):
        self.set_target(0, 0)
        self._move_timeout = 0

    def forward(self):
        left = self.moving_power * min(self.balance, 50) / 50.0
        right = self.moving_power * min(100 - self.balance, 50) / 50.0
        self.set_target(left, right)
        self._move_timeout = int(time.time()*1000) + self.moving_time

    def left(self):
        left = self.turning_power
        right = - self.turning_power
        self.set_target(left, right)
        self._move_timeout = int(time.time()*1000) + self.turning_time

    def right(self):
        left = - self.turning_power
        right = self.turning_power
        self.set_target(left, right)
        self._move_timeout = int(time.time()*1000) + self.turning_time

    def back(self):
        left = - (self.moving_power * min(self.balance, 50) / 50.0)
        right = - (self.moving_power * min(100 - self.balance, 50) / 50.0)
        self.set_target(left, right)
        self._move_timeout = int(time.time()*1000) + self.moving_time

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
            self.forward()
        elif message == 'back':
            self.back()
        elif message == 'left':
            self.left()
        elif message == 'right':
            self.right()
        elif message == 'stop':
            self.brake()
        elif message == 'quit':
            self.brake()
            quit()
        else:
            print("broadcast(%s)" % message)

    def set_variable(self, _key, val):
        key = _key.encode('utf-8').replace(' ','').lower()
        if key == 'moving_time':
            self.moving_time = int(val)
        elif key == 'moving_power':
            self.moving_power = min(max(int(val),-100),100)
        elif key == 'balance':
            self.balance = min(max(int(val),0),100)
        elif key == 'turning_time':
            self.turning_time = int(val)
        elif key == 'turning_power':
            self.turning_power = min(max(int(val),0),100)
        elif key == 'interval':
            self.interval = min(max(int(val),0),100)
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

def testCallback(left, right):
    print "TW:", left, right

if __name__ == '__main__':
    rc = RobotController()
    rc.forward()
    for i in range(10):
        rc.update_current()
    rc.left()
    for i in range(10):
        rc.update_current()
    for i in range(10):
        rc.spinOnce()
        time.sleep(0.3)

