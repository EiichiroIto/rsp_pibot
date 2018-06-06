from threading import Thread, Event
import time

class Vehicle(object):
    def __init__(self, device, server):
        self.device = device
        self.set_server(server)
        self.thread_interval = 200 # parameter (ms)
        self._thread = None
        self._handlers = {}
        self._variables = {}
        self._sensors = {}
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

    def add_sensor(self, key, func):
        self._sensors[key] = func

    def _send_sensor_values(self):
        _sensors = {}
        _broadcasts = []
        for k in self._sensors:
            dict = self._sensors[k].values()
            if len(dict) > 0:
                _sensors.update(dict)
                _broadcasts.append(k)
        if len(_sensors) > 0:
            self.server.send_sensor_update(_sensors)
        for b in _broadcasts:
            self.server.send_broadcast(b)

    def timer_thread(self):
        while not self.stop_event.is_set():
            self.spin_once()
            self._send_sensor_values()
            time.sleep(self.thread_interval/1000.0)

    def spin_once(self):
        pass

    def start(self):
        if self._thread is not None:
            return
        self.stop_event = Event()
        self._thread = Thread(target=self.timer_thread)
        self._thread.daemon = False #True
        self._thread.start()
        for k in self._sensors:
            self._sensors[k].start()
        if self.server is not None:
            self.server.start()

    def stop(self):
        self.stop_event.set()
        self._thread.join()
        self._thread = None
        if self.server is not None:
            self.server.stop()
        for k in self._sensors:
            self._sensors[k].stop()

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
            while not self.stop_event.is_set():
		time.sleep(1)
        finally:
            self.stop()

if __name__ == '__main__':
    car = Vehicle(device=None, server=None)
    car.broadcast('forward')
