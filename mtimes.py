import time
import datetime 




class Signal:
    
    def __init__(self, interval_sec:float=1) -> None:
        self.current = time.monotonic()
        self.interval = interval_sec
        self.__LOCK = False
        self.__START = False
    
    def is_stop(self):
        return not self.__LOCK
    
    def start(self, interval_sec:float=None):
        if not self.__LOCK:
            if interval_sec is not None:
                self.interval = interval_sec
            self.current = time.monotonic()
            self.__LOCK = True

    def stop(self):
        if self.__LOCK:
            if time.monotonic() - self.current >= self.interval:
                self.__LOCK = False
                return True
        return False


class Timer:
    
    def __init__(self) -> None:
        self.START = False
        self.current_time = None
    
    def set_start_value(self, hours=0, minutes=0, seconds=0):
        self.hours = hours
        self.minutes = minutes
        self.seconds = seconds
    
    def start(self):
        if not self.START:
            self.current_time = ...

    
    def iter_time(self):
        ...


if __name__ == "__main__":
    t = Signal(3)