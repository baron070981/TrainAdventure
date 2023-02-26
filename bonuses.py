import pygame
from pathlib import Path
import time

from rich import inspect, print

from mtimes import Signal

class BaseBonuseX(pygame.sprite.Sprite):
    
    def __init__(self, speed_anim=1, idn='bonus') -> None:
        super().__init__()
        self.ext = ['.jpg', '.png']
        self.files = []
        self.dir_images = None
        self.speed_anim = speed_anim
        self.surfs = None
        self.index = 0
        self.__repetition_counter = 0
        self.image = None
        self.rect = None
        self.idn = idn

    
    def init_dir(self, dir_images, size, pos=(0, 0), speed_anim=None):
        if speed_anim is not None:
            self.speed_anim = speed_anim
        self.size = size
        self.pos = pos
        self.dir_images = dir_images
        self.files = self.get_files(self.dir_images)
        surfs = [pygame.image.load(str(f)).convert_alpha() for f in self.files]
        self.surfs = list(map(lambda x: pygame.transform.scale(x, size), surfs))
        self.image = self.surfs[self.index].copy()
        self.rect = self.image.get_rect(center=pos)
    
    
    def init_list(self, list_images, size, pos=(0,0), speed_anim=None):
        if speed_anim is not None:
            self.speed_anim = speed_anim
        self.pos = pos
        self.size = size
        self.files = list_images.copy()
        surfs = [pygame.image.load(str(f)).convert_alpha() for f in self.files]
        self.surfs = list(map(lambda x: pygame.transform.scale(x, size), surfs))
        self.image = self.surfs[self.index].copy()
        self.rect = self.image.get_rect(center=pos)

    def set_attrs(self, **kwargs):
        size = kwargs.get('size', None)
        if size is not None:
            self.size = size
            self.pos = self.rect.center
            self.surfs = list(map(lambda x: pygame.transform.scale(x, size), self.surfs))
            self.image = self.surfs[self.index]
            self.rect = self.image.get_rect(x=self.pos[0], y=self.pos[1])
    
    def get_files(self, dir_files):
        dir_files = Path(dir_files)
        files = dir_files.iterdir()
        files = list(filter(lambda x: x.suffix in self.ext, files))
        files = sorted(files)
        return files
    
        
    def iter_surfs(self):
        self.__repetition_counter += 1
        index = self.index
        if self.__repetition_counter >= self.speed_anim:
            print('INDEX ++')
            index += 1
            self.__repetition_counter = 0
        if index >= len(self.surfs) - 1:
            print('INDEX == 0')
            index = 0
        if index != self.index:
            print('New IMAGE')
            self.index = index
            self.image = self.surfs[index]
    
    
    def set_position(self, pos):
        self.pos = pos
        self.rect = self.image.get_rect(center=pos)
    

class BaseBonuse(pygame.sprite.Sprite):
    
    def __init__(self, id_name) -> None:
        super().__init__()
        self.index = 0
        self.timer = Signal()
        self.id_name = id_name

    
    def init_list(self, files_list:list, size:tuple, pos:tuple=(0,0), speed:float=1):
        self.speed = speed
        self.pos = pos
        self.size = size
        self.files = files_list.copy()
        surfs = [pygame.image.load(str(f)).convert_alpha() for f in self.files]
        self.surfs = list(map(lambda x: pygame.transform.scale(x, size), surfs))
        self.image = self.surfs[self.index].copy()
        self.rect = self.image.get_rect(center=pos)
        self.timer.interval = speed
    
    def set_attrs(self, **kwargs):
        size = kwargs.get('size', None)
        if size is not None:
            self.size = size
            self.pos = self.rect.center
            self.surfs = list(map(lambda x: pygame.transform.scale(x, (size, size)), self.surfs))
            self.image = self.surfs[self.index]
            self.rect = self.image.get_rect(x=self.pos[0], y=self.pos[1])
    
    def set_position(self, pos):
        self.pos = pos
        self.rect = self.image.get_rect(center=pos)
    
    
    def iter_surfs(self):
            self.timer.start()
            self.timer.stop()
            if self.timer.is_stop():
                self.index += 1
                if self.index >= len(self.files):
                    self.index = 0
                self.image = self.surfs[self.index]
    


    





if __name__ == "__main__":
    ...
    pygame.init()
    dispinfo = pygame.display.Info()
    SCREEN_SIZE = (dispinfo.current_w-15, dispinfo.current_h-15)
    screen = pygame.display.set_mode((SCREEN_SIZE), pygame.DOUBLEBUF | pygame.RESIZABLE | pygame.NOFRAME)
    
    
    b = BaseBonuse()
    b.init_dir('./media/bullets_bonus', (10,10), speed_anim=5)
    # cnt = 0
    # while True:
    #     cnt += 1
    #     if cnt >= 100:
    #         break
    #     b.iter_surfs()
    #     time.sleep(.5)

