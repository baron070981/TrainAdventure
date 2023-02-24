import pygame
from pathlib import Path
from rich import inspect, print


class Explosion(pygame.sprite.Sprite):
    
    def __init__(self, size:tuple, files:list, start=False) -> None:
        super().__init__()
        self.size = size
        surfaces = [pygame.image.load(e).convert_alpha() for e in files]
        self.surfaces = list(map(lambda x: pygame.transform.scale(x, size), surfaces))
        self.image = self.surfaces[0]
        self.rect = self.image.get_rect(x=0, y=0)
        self.index = 0
        self.start = start
    
    
    def iter_surface(self):
        if self.start:
            self.image = self.surfaces[self.index]
            self.index += 1
            if self.index >= len(self.surfaces):
                self.index = 0
                self.start = False

    def set_position(self, position):
        self.rect = self.image.get_rect(center=position)




if __name__ == "__main__":
    ...


    
