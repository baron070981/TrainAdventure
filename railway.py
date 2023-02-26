from pathlib import Path
from abc import ABC, abstractmethod
import enum
from dataclasses import dataclass
from random import randint, choice

import pygame


@dataclass(frozen=True)
class RWEnum:
    TURN_LB = 1
    TURN_RB = 2
    TURN_LT = 3
    TURN_RT = 4
    STRAIGHT_LR = 1
    STRAIGHT_TB = 2
    ARROW_LTB = 1
    ARROW_LTR = 2
    ARROW_LBR = 3
    ARROW_RBT = 4
    DIR_UP = 1
    DIR_DOWN = 2
    DIR_LEFT = 3
    DIR_RIGHT = 4
    ARROW_TURN_L = 1
    ARROW_TURN_R = 2


@dataclass
class RWDirection:
    DIR_UP = 1
    DIR_DOWN = 2
    DIR_LEFT = 3
    DIR_RIGHT = 4



class BaseMapElements(ABC):
    
    @abstractmethod
    def move(self, x, y, direct, **kwargs):
        ...

    @abstractmethod
    def is_collide(self, point):
        ...


class RailWay(ABC, pygame.sprite.Sprite):
    # общий класс для всех видов жд путей(повороты, прямые, стрелки...)
    def __init__(self, filename, name, pos=None, size=None, speed=3, **kwargs):
        super().__init__()
        self.__image =  pygame.image.load(filename).convert_alpha()
        self.__pos = pygame.Vector2((0, 0)) if pos is None \
                                            else pygame.Vector2(pos)
        self.__name = name
        if size is not None:
            self.image = pygame.transform.scale(self.__image.copy(), size)
        else:
            self.image = self.__image.copy()
        self.size = size
        x,y = self.__pos
        self.rect = self.image.get_rect(x=x, y=y)
        self.speed = speed
        match name:
            case 'line_tb':
                self.opt = choice([RWDirection.DIR_DOWN, RWDirection.DIR_UP])
            case 'line_lr':
                self.opt = choice([RWDirection.DIR_LEFT, RWDirection.DIR_RIGHT])
            case _:
                self.opt = 1
        self.draw_flag = True
    
    
    @property
    def name(self):
        return self.__name
    
    
    @abstractmethod
    def move(self, x, y, direction):
        '''Опрделяет правила по котррым будет двигаться поезд.'''
    
    
    def update(self):
        if not self.draw_flag:
            s = self.rect.width
            h = self.rect.height
            pygame.draw.rect(self.image, (250,20,20), (0, 0, s, h), 2)
            self.draw_flag = True
    
    
    def is_collide(self, point: tuple):
        return self.rect.collidepoint(*point)
    
    
    def get_controls(self):
        return self.speed


class StraightSection(RailWay):
    # прямой учаток дороги
    ...
    def get_opt(self):
        return randint(1, 4)
    
    
    def move(self, x, y, direction):
        match direction:
            case RWDirection.DIR_LEFT:
                return x - self.speed, y, direction
            case RWDirection.DIR_RIGHT:
                return x + self.speed, y, direction
            case RWDirection.DIR_UP:
                return x, y - self.speed, direction
            case RWDirection.DIR_DOWN:
                return x, y + self.speed, direction
    

class RWTurn(BaseMapElements, pygame.sprite.Sprite):
    
    def __init__(self, filename, name, size=None, pos=None, speed=3) -> None:
        super().__init__()
        self.filename = filename
        self.name = name
        self.pos = (0,0) if pos is None else pos
        self.speed = speed
        image = pygame.image.load(self.filename).convert_alpha()
        if size is not None:
            self.image = pygame.transform.scale(image.copy(), size)
        else:
            self.image = image.copy()
        self.rect = self.image.get_rect(x=pos[0], y=pos[1])
        self.size = self.image.get_size()
        self.direct = RWDirection.DIR_LEFT
    
    
    def is_collide(self, point):
        return self.rect.collidepoint(*point)
    
    
    def move(self, x, y, direct, **kwargs):
        speed = kwargs.get('speed', self.speed)
        match self.name:
            case 'turn_lt':
                if direct == RWDirection.DIR_RIGHT or direct == RWDirection.DIR_UP:
                    if x < self.rect.center[0]:
                        x += speed
                    elif x >= self.rect.center[0]:
                        y -= speed
                        x = self.rect.center[0]
                        direct = RWDirection.DIR_UP
                elif direct == RWDirection.DIR_LEFT or direct == RWDirection.DIR_DOWN:
                    if y < self.rect.center[1]:
                        y += speed
                    elif y >= self.rect.center[1]:
                        x -= speed
                        y = self.rect.center[1]
                        direct = RWDirection.DIR_LEFT
            # поворот слева вниз и снизу влево
            case 'turn_lb':
                if direct == RWDirection.DIR_RIGHT or direct == RWDirection.DIR_DOWN:
                    if x < self.rect.center[0]:
                        x += speed
                    elif x >= self.rect.center[0]:
                        y += speed
                        x = self.rect.center[0]
                        direct = RWDirection.DIR_DOWN
                elif direct == RWDirection.DIR_LEFT or direct == RWDirection.DIR_UP:
                    if y > self.rect.center[1]:
                        y -= speed
                    elif y <= self.rect.center[1]:
                        x -= speed
                        y = self.rect.center[1]
                        direct = RWDirection.DIR_LEFT
            # поворот справа вверх и сверху вправо
            case 'turn_rt':
                if direct == RWDirection.DIR_LEFT or direct == RWDirection.DIR_UP:
                    if x > self.rect.center[0]:
                        x -= speed
                    elif x <= self.rect.center[0]:
                        y -= speed
                        x = self.rect.center[0]
                        direct = RWDirection.DIR_UP
                elif direct == RWDirection.DIR_RIGHT or direct == RWDirection.DIR_DOWN:
                    if y < self.rect.center[1]:
                        y += speed
                    elif y >= self.rect.center[1]:
                        x += speed
                        y = self.rect.center[1]
                        direct = RWDirection.DIR_RIGHT
            # поворот справа вниз и снизу вправо
            case 'turn_rb':
                if direct == RWDirection.DIR_LEFT or direct == RWDirection.DIR_DOWN:
                    if x > self.rect.center[0]:
                        x -= speed
                    elif x <= self.rect.center[0]:
                        y += speed
                        x = self.rect.center[0]
                        direct = RWDirection.DIR_DOWN
                elif direct == RWDirection.DIR_RIGHT or direct == RWDirection.DIR_UP:
                    if y > self.rect.center[1]:
                        y -= speed
                    elif y <= self.rect.center[1]:
                        x += speed
                        y = self.rect.center[1]
                        direct = RWDirection.DIR_RIGHT
        return x, y, direct


class RWStraightSection(BaseMapElements, pygame.sprite.Sprite):
    names = ['line_tb', 'line_lr']
    def __init__(self, filename, name, size=None, pos=None, speed=3) -> None:
        super().__init__()
        self.filename = filename
        self.name = name
        self.pos = (0,0) if pos is None else pos
        self.speed = speed
        image = pygame.image.load(self.filename).convert_alpha()
        if size is not None:
            self.image = pygame.transform.scale(image.copy(), size)
        else:
            self.image = image.copy()
        self.rect = self.image.get_rect(x=pos[0], y=pos[1])
        self.size = self.image.get_size()
        match self.name:
            case 'line_tb':
                self.direct = choice([RWDirection.DIR_DOWN, RWDirection.DIR_UP])
            case 'line_lr':
                self.direct = choice([RWDirection.DIR_LEFT, RWDirection.DIR_RIGHT])
            case _:
                raise ValueError(f'Не возможно определить имя. Доступные имена {RWStraightSection.names}')
    
    
    def is_collide(self, point:tuple):
        return self.rect.collidepoint(*point)

    def move(self, x, y, direct, **kwargs):
        speed = kwargs.get('speed', self.speed)
        match self.name:
            # прямая слева на прово
            case 'line_lr':
                if direct == RWDirection.DIR_LEFT:
                    x -= speed
                elif direct == RWDirection.DIR_RIGHT:
                    x += speed
            # прямая сверху вниз
            case 'line_tb':
                if direct == RWDirection.DIR_UP:
                    y -= speed
                elif direct == RWDirection.DIR_DOWN:
                    y += speed
        return x, y, direct
    

class RWArrow(BaseMapElements, pygame.sprite.Sprite):
    
    TURN_FLAGS = [RWEnum.ARROW_TURN_L, RWEnum.ARROW_TURN_R]
    
    def __init__(self, filename, name, **kwargs):
        """
filename:str - путь к изображению со стрелкой с открытым поворотом влево
name:str - имя данного спрайта, желательно чтоб совпадало с тегом name в xml файле карты
kwargs:
    right:str - путь к изображению со стрелкой с открытым поворотом вправо
    size:tuple - размер к которому следует привести спрайт
    pos:tupe - позиция спрайта
    speed:int - скорость с которой движется паравозик, если паравозик не передаст свою скорость
"""
        super().__init__()
        left = filename
        self.turn = choice(RWArrow.TURN_FLAGS)
        right = kwargs.get('right', filename)
        self.left = pygame.image.load(left).convert_alpha()
        self.right = pygame.image.load(right).convert_alpha()
        self.size = kwargs.get('size', (30,30))
        self.__pos = kwargs.get('pos', (0,0))
        self.speed = kwargs.get('speed', 1)
        image = self.left.copy() if self.turn == RWEnum.ARROW_TURN_L else self.right.copy()
        self.image = pygame.transform.scale(image.copy(), self.size)
        self.__name = name
        x, y = self.__pos
        self.rect = self.image.get_rect(x=x, y=y)
    
    
    @property
    def name(self):
        return self.__name
    
    def move(self, x, y, direct, **kwargs):
        speed = kwargs.get('speed', self.speed)
        match self.__name:
            case 'arrow_lb_rb_lr':
                # с открытым правым поворотом
                if self.turn == RWEnum.ARROW_TURN_R:
                    if direct == RWDirection.DIR_LEFT or direct == RWDirection.DIR_DOWN:
                        if x > self.rect.center[0]:
                            x -= speed
                        elif x <= self.rect.center[0]:
                            y += speed
                            x = self.rect.center[0]
                            direct = RWDirection.DIR_DOWN
                    elif direct == RWDirection.DIR_RIGHT or direct == RWDirection.DIR_UP:
                        if y > self.rect.center[1]:
                            y -= speed
                        elif y <= self.rect.center[1]:
                            x += speed
                            y = self.rect.center[1]
                            direct = RWDirection.DIR_RIGHT
                    elif direct == RWDirection.DIR_RIGHT:
                        x += speed
                # с открытым левым поворотом
                if self.turn == RWEnum.ARROW_TURN_L:
                    if direct == RWDirection.DIR_RIGHT or direct == RWDirection.DIR_DOWN:
                        if x < self.rect.center[0]:
                            x += speed
                        elif x >= self.rect.center[0]:
                            y += speed
                            x = self.rect.center[0]
                            direct = RWDirection.DIR_DOWN
                    elif direct == RWDirection.DIR_LEFT or direct == RWDirection.DIR_UP:
                        if y > self.rect.center[1]:
                            y -= speed
                        elif y <= self.rect.center[1]:
                            x -= speed
                            y = self.rect.center[1]
                            direct = RWDirection.DIR_LEFT
                    elif direct == RWDirection.DIR_LEFT:
                        x -= speed
            
            case 'arrow_lt_rt_lr':
                if self.turn == RWEnum.ARROW_TURN_L:
                    if direct == RWDirection.DIR_LEFT or direct == RWDirection.DIR_UP:
                        if x > self.rect.center[0]:
                            x -= speed
                        elif x <= self.rect.center[0]:
                            y -= speed
                            x = self.rect.center[0]
                            direct = RWDirection.DIR_UP
                    elif direct == RWDirection.DIR_RIGHT or direct == RWDirection.DIR_DOWN:
                        if y < self.rect.center[1]:
                            y += speed
                        elif y >= self.rect.center[1]:
                            x += speed
                            y = self.rect.center[1]
                            direct = RWDirection.DIR_RIGHT
                    elif direct == RWDirection.DIR_RIGHT:
                        x += speed
                elif self.turn == RWEnum.ARROW_TURN_R:
                    if direct == RWDirection.DIR_RIGHT or direct == RWDirection.DIR_UP:
                        if x < self.rect.center[0]:
                            x += speed
                        elif x >= self.rect.center[0]:
                            y -= speed
                            x = self.rect.center[0]
                            direct = RWDirection.DIR_UP
                    elif direct == RWDirection.DIR_LEFT or direct == RWDirection.DIR_DOWN:
                        if y < self.rect.center[1]:
                            y += speed
                        elif y >= self.rect.center[1]:
                            x -= speed
                            y = self.rect.center[1]
                            direct = RWDirection.DIR_LEFT
                    elif direct == RWDirection.DIR_LEFT:
                        x -= speed
            
            case 'arrow_rt_rb_tb':
                if self.turn == RWEnum.ARROW_TURN_L:
                    if direct == RWDirection.DIR_LEFT or direct == RWDirection.DIR_DOWN:
                        if x > self.rect.center[0]:
                            x -= speed
                        elif x <= self.rect.center[0]:
                            y += speed
                            x = self.rect.center[0]
                            direct = RWDirection.DIR_DOWN
                    elif direct == RWDirection.DIR_RIGHT or direct == RWDirection.DIR_UP:
                        if y > self.rect.center[1]:
                            y -= speed
                        elif y <= self.rect.center[1]:
                            x += speed
                            y = self.rect.center[1]
                            direct = RWDirection.DIR_RIGHT
                    elif direct == RWEnum.DIR_DOWN:
                        y += speed
                elif self.turn == RWEnum.ARROW_TURN_R:
                    if direct == RWDirection.DIR_LEFT or direct == RWDirection.DIR_UP:
                        if x > self.rect.center[0]:
                            x -= speed
                        elif x <= self.rect.center[0]:
                            y -= speed
                            x = self.rect.center[0]
                            direct = RWDirection.DIR_UP
                            
                    elif direct == RWDirection.DIR_RIGHT or direct == RWDirection.DIR_DOWN:
                        if y < self.rect.center[1]:
                            y += speed
                        elif y >= self.rect.center[1]:
                            x += speed
                            y = self.rect.center[1]
                            direct = RWDirection.DIR_RIGHT
                        
                    elif direct == RWEnum.DIR_UP:
                        y -= speed
            
            case 'arrow_lt_lb_tb':
                if self.turn == RWEnum.ARROW_TURN_L:
                    if direct == RWDirection.DIR_RIGHT or direct == RWDirection.DIR_UP:
                        if x < self.rect.center[0]:
                            x += speed
                        elif x >= self.rect.center[0]:
                            y -= speed
                            x = self.rect.center[0]
                            direct = RWDirection.DIR_UP
                    elif direct == RWDirection.DIR_LEFT or direct == RWDirection.DIR_DOWN:
                        if y < self.rect.center[1]:
                            y += speed
                        elif y >= self.rect.center[1]:
                            x -= speed
                            y = self.rect.center[1]
                            direct = RWDirection.DIR_LEFT
                    elif direct == RWDirection.DIR_UP:
                        y -= speed
                
                if self.turn == RWEnum.ARROW_TURN_R:
                    if direct == RWDirection.DIR_RIGHT or direct == RWDirection.DIR_DOWN:
                        if x < self.rect.center[0]:
                            x += speed
                        elif x >= self.rect.center[0]:
                            y += speed
                            x = self.rect.center[0]
                            direct = RWDirection.DIR_DOWN
                    elif direct == RWDirection.DIR_LEFT or direct == RWDirection.DIR_UP:
                        if y > self.rect.center[1]:
                            y -= speed
                        elif y <= self.rect.center[1]:
                            x -= speed
                            y = self.rect.center[1]
                            direct = RWDirection.DIR_LEFT
                        return x, y, direct
                    elif direct == RWDirection.DIR_DOWN:
                        y += speed
                    
        return x, y, direct
    
    
    def set_turn(self, turn):
        if turn not in RWArrow.TURN_FLAGS:
            raise ValueError('')
        if turn != self.turn:
            self.turn = turn
            image = self.left if turn == RWEnum.ARROW_TURN_L else self.right
            self.image = pygame.transform.scale(image.copy(), self.size)
        x, y = self.__pos
        self.rect = self.image.get_rect(x=x, y=y)
    
    
    def is_collide(self, point: tuple):
        return self.rect.collidepoint(*point)
    
    
    def reset_turn(self):
        turn = choice(RWArrow.TURN_FLAGS)
        self.set_turn(turn)
    
    
    def reset_turn2(self):
        turn = RWEnum.ARROW_TURN_L if self.turn == RWEnum.ARROW_TURN_R else RWEnum.ARROW_TURN_R
        self.set_turn(turn)


class DecorMapElement(BaseMapElements, pygame.sprite.Sprite):
    
    def __init__(self, filename, name, **kwargs) -> None:
        super().__init__()
        size = kwargs.get('size', None)
        self.pos = kwargs.get('pos', (0, 0))
        self.name = name
        self.filename = filename
        image = pygame.image.load(filename).convert_alpha()
        if size:
            self.image = pygame.transform.scale(image.copy(), size)
        else:
            self.image = image.copy()
        self.size = self.image.get_size()
        self.rect = self.image.get_rect(x=self.pos[0], y=self.pos[1])
    
    def move(self, x, y, direct, **kwargs):
        return x, y, direct
    
    def is_collide(self, point):
        return False


    

if __name__ == "__main__":
    ...
    data = {'size':(10,10), 'pos':(0,3), 'speed':27}
    line = RWStraightSection('a', 'b', **data)
    
    
    
    
    
    
    
    
    
    
    
    







