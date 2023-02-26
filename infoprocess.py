import pygame
from pathlib import Path
from rich import inspect, print

class LocoLifeInfo(pygame.sprite.Sprite):
    
    def __init__(self, pos:tuple, size:tuple, life:int, files:list) -> None:
        super().__init__()
        surfaces = [pygame.image.load(e).convert_alpha() for e in files]
        self.surfaces = list(map(lambda x: pygame.transform.scale(x, size), surfaces))
        self.image = self.surfaces[-1]
        self.rect = self.image.get_rect(x=pos[0], y=pos[1])
    
    
    def set_life(self, life:int):
        # life - int - от 1
        if life < 0:
            life = 0
        elif life > len(self.surfaces):
            life = len(self.surfaces)
        self.image = self.surfaces[life-1]


class BulletsInfo(pygame.sprite.Sprite):
    
    def __init__(self, pos:tuple, size:tuple, file:str|pygame.Surface, val=0):
        super().__init__()
        image = None
        self.size = size
        self.pos = pos
        self.val = val
        if isinstance(file, str):
            image = pygame.image.load(file).convert_alpha()
        
        self.obj_font = pygame.font.Font(None, 48)
        self.text = self.obj_font.render(str(self.val), 1, (255, 20, 20))
        self.image = pygame.transform.scale(image.copy(), size)
        self.rect = self.image.get_rect(x=pos[0], y=pos[1])
        self.text_rect = self.image.get_rect(x=pos[0]+size[0], y=pos[1])
    
    def set_value(self, val):
        self.val = val
        self.text = self.obj_font.render(str(val), 1, (255, 20, 20))
    
    
    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))
        screen.blit(self.text, (self.text_rect.x, self.text_rect.y))


class CoinsInfo(pygame.sprite.Sprite):
    
    def __init__(self, pos:tuple, size:tuple, file:str|pygame.Surface, val=0):
        super().__init__()
        image = None
        self.size = size
        self.pos = pos
        self.val = val
        if isinstance(file, str):
            image = pygame.image.load(file).convert_alpha()
        
        self.obj_font = pygame.font.Font(None, 48)
        self.text = self.obj_font.render(str(self.val), 1, (255, 20, 20))
        self.image = pygame.transform.scale(image.copy(), size)
        self.rect = self.image.get_rect(x=pos[0], y=pos[1])
        self.text_rect = self.image.get_rect(x=pos[0]+size[0], y=pos[1])

    
    def set_value(self, val):
        self.val = val
        self.text = self.obj_font.render(str(val), 1, (255, 20, 20))
    
    
    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))
        screen.blit(self.text, (self.text_rect.x, self.text_rect.y))
    
    


if __name__ == "__main__":
    ...



 
