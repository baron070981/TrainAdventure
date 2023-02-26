import pygame
from pathlib import Path
from rich import inspect, print

import mtimes

class Explosion(pygame.sprite.Sprite):
    
    def __init__(self, size:tuple, files:list, start=False, speed=.1) -> None:
        super().__init__()
        self.size = size
        surfaces = [pygame.image.load(e).convert_alpha() for e in files]
        self.surfs = list(map(lambda x: pygame.transform.scale(x, size), surfaces))
        self.index = 0
        self.files = files.copy()
        self.start = start
        self.speed = speed
        self.timer = mtimes.Signal(speed)
        self.index = 0
        self.image = self.surfs[self.index]
        self.rect = self.image.get_rect(x=0, y=0)
    
    
    def iter_surfacex(self):
        if self.start:
            self.image = self.surfaces[self.index]
            self.index += 1
            if self.index >= len(self.surfaces):
                self.index = 0
                self.start = False

    
    def set_attrs(self, **kwargs):
        size = kwargs.get('size', None)
        if size is not None:
            self.size = (size, size)
            self.pos = self.rect.center
            self.surfs = list(map(lambda x: pygame.transform.scale(x, (size, size)), self.surfs))
            self.image = self.surfs[self.index]
            self.rect = self.image.get_rect(x=self.pos[0], y=self.pos[1])
    
    
    def iter_surface(self):
        self.timer.start()
        self.timer.stop()
        if self.timer.is_stop():
            self.index += 1
        if self.index >= len(self.files):
            self.index = 0
            self.start = False
            return
        self.image = self.surfs[self.index]
    
    
    def set_position(self, position):
        self.rect = self.image.get_rect(center=position)



if __name__ == "__main__":
    ...


    
