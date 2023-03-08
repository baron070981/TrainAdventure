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
        self.START = False # запущен ли таймер
        self.STOP = True # таймер остановлен
        self.hours = 0
        self.minutes = 0
        self.seconds = 0
        self.interval_sec = 0 # время работы таймера в секундах
        self.start_time = 0 # время начала работы таймера в секундах
        self.delta = 0
    
    # установка времени через которое сработает таймер
    def set_start_value(self, hours=0, minutes=0, seconds=0):
        self.hours = hours
        self.minutes = minutes
        self.seconds = seconds
        # время работы таймера в секундах
        self.interval_sec = hours * 60 + minutes * 60 + seconds
    
    # запуск таймера
    def start(self):
        if not self.START:
            self.START = True
            self.STOP = False
            self.start_time = time.time()
    
    # обновление прошедшего времени
    def iter_time(self):
        if self.START:
            print('iter')
            self.delta = time.time() - self.start_time
            if self.interval_sec - self.delta <= 0:
                print('End limit time')
                self.START = False
                self.STOP = True
                self.delta = 0
    
    # получение оставшегося времени
    def get_remaining_time(self):
        t = self.interval_sec - self.delta
        seconds = int(t - t // 60 * 60)
        t -= seconds
        minute = int(t // 60 - t // 3600 * 60)
        hour = int(t // 3600)
        return hour, minute, seconds
    
    # остановка и сброс таймера
    def stop(self):
        print('Calling timer.stop function')
        self.STOP = True
        self.START = False
        self.delta = 0
        self.start_time = 0
        


if __name__ == "__main__":
    ...
    
    t = Timer()
    t.set_start_value(minutes=1)
    while True:
        t.start()
        t.iter_time()
        if t.STOP:
            print('Stop timer')
            break
        rt = t.get_remaining_time()
        print(f'{rt[0]}:{rt[1]}:{rt[2]}')
    
    