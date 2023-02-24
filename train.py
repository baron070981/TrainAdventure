from pathlib import Path
from abc import ABC, abstractmethod

import pygame
from rich import print
from railway import RWEnum, RWDirection



class FireBall(pygame.sprite.Sprite):
    
    def __init__(self, file, pos:tuple, size:tuple, direct:RWDirection, speed:int=1) -> None:
        super().__init__()
        self.speed = speed
        self.direct = direct
        self.pos = pos
        self.size = size
        self.start_life_count = 100
        self.__life_count = self.start_life_count
        self.is_live = False
        image = None
        if isinstance(file, (str, Path)):
            image = pygame.image.load(str(file)).convert_alpha()
        elif isinstance(file, pygame.Surface):
            image = file.copy()
        else:
            raise ValueError('Параметр file должен быть строкой, Path или pygame.Surface')
        self.image = pygame.transform.scale(image, self.size)
        self.rect = self.image.get_rect(x=pos[0], y=pos[1])
    
    
    def is_collide(self, point):
        ...
    
    def reset(self, pos=(0,0)):
        self.__life_count = self.start_life_count
        self.is_live = False
        self.rect = self.image.get_rect(x=pos[0], y=pos[1])
    
    
    def move(self, speed=0):
        x, y, w, h = self.rect
        self.__life_count -= 1
        match self.direct:
            case RWDirection.DIR_LEFT:
                x -= (self.speed + speed)
            case RWDirection.DIR_RIGHT:
                x += (self.speed + speed)
            case RWDirection.DIR_UP:
                y -= (self.speed + speed)
            case RWDirection.DIR_DOWN:
                y += (self.speed + speed)
        self.rect = self.image.get_rect(x=x, y=y)
    
    @property
    def is_life_count(self):
        return self.__life_count > 0
    
    
    
        
        
class Clip:
    ...


class Locomotive(pygame.sprite.Sprite):
    
    def __init__(self, pos, size, left, up=None, 
                 right=None, down=None, speed=3,  
                 direct=RWDirection.DIR_LEFT, decrease=1):
        super().__init__()
        self.__pos = pos
        self.size = size
        self.life = 5
        self.max_bullets = 5
        self.bullets = 5
        self.coins = 0
        self.decrease = decrease
        self.__images = {
                RWDirection.DIR_LEFT: left,
                RWDirection.DIR_UP: up if up is not None else left,
                RWDirection.DIR_RIGHT: right if right is not None else left,
                RWDirection.DIR_DOWN: down if down is not None else left
            }
        self.direct = direct
        self.speed = speed
        self.__image = self.__images[direct].copy()
        self.image = pygame.transform.scale(self.__image.copy(), (size, size))
        self.rect = self.image.get_rect(center=pos)
    
    
    def set_direct(self, direct):
        self.direct = direct
        self.__image = self.__images[direct].copy()
        self.image = pygame.transform.scale(self.__image.copy(), (self.size, self.size))
    
    @property
    def current_pos(self):
        return self.rect.center
    
    
    @current_pos.setter
    def current_pos(self, pos):
        self.rect.center = pos
    
    
    def move(self, x, y, size, direction):
        if direction != self.direct:
            self.direct = direction
            self.__image = self.__images[direction].copy()
            self.image = pygame.transform.scale(self.__image.copy(), (self.size, self.size))
        self.rect = self.image.get_rect(center=(x, y))
    
    
    def update(self):
        ...
    
    
    def is_live(self):
        return self.life > 0
    
    def decrease_life(self):
        self.life -= self.decrease
    
    def is_collide(self, point):
        return self.rect.collidepoint(*point)

    def shoot(self):
        self.bullets -= 1 if self.bullets > 0 else 0

    def reload_gun(self):
        self.bullets = self.max_bullets
    
    def recovery_life(self):
        self.life = 5







if __name__ == "__main__":
    ...
    
    
    
    







