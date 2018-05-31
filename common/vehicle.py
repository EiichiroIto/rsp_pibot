from threading import Thread
import time

class Vehicle(object):
    def __init__(self, device, server):
        self.device = device
        self.set_server(server)
        self.thread_interval = 200 # parameter (ms)
        self._thread = None
        self._quit_loop = False
        self._handlers = {}
        self._variables = {}
        self.add_variable('thread_interval', self.set_thread_interval)
        self.setup()

    def setup(self):
        pass

    def set_server(self, server):
        self.server = server
        if self.server is not None:
            self.server.set_controller(self)

    def add_handler(self, key, func):
        self._handlers[key] = func

    def add_variable(self, key, func):
        self._variables[key] = func

    def timer_thread(self):
        while self._thread is not None:
            self.spin_once()
            time.sleep(self.thread_interval/1000.0)

    def spin_once(self):
        pass

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

    def sensor_update(self, list):
        for (k,v) in list:
            print(k)
            key = k.encode('utf-8').replace(' ','').lower()
            if key in self._variables:
                if type(v) is unicode:
                    val = v.encode('utf-8')
                else:
                    val = str(v)
                self._variables[key](val)
            else:
                print("sensor_update(%s)" % key)

    def broadcast(self, m):
        message = m.encode('utf-8').replace(' ','').lower()
        if message in self._handlers:
            self._handlers[message]()
        else:
            print("broadcast(%s)" % message)

    def set_thread_interval(self, val):
        self.thread_interval = min(max(int(val),0),100)

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

if __name__ == '__main__':
    car = Vehicle(device=None, server=None)
    car.broadcast('forward')
