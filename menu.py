import pygame
from pathlib import Path
from rich import inspect, print


class MiniMap(pygame.sprite.Sprite):
    
    def __init__(self, filename, mapfile, size:tuple=None, pos:tuple=None) -> None:
        super().__init__()
        self.filename = filename
        self.mapfile = mapfile
        self.pos = (0,0) if pos is None else pos
        image = pygame.image.load(str(filename)).convert_alpha()
        if size:
            self.image = pygame.transform.scale(image.copy(), size)
        else:
            self.image = image.copy()
        self.size = self.image.get_size()
        self.rect = self.image.get_rect(x=pos[0], y=pos[1])
        s = self.rect.width
        h = self.rect.height
        pygame.draw.rect(self.image, (250,20,20), (0, 0, s, h), 2)

    
    def is_collide(self, point:tuple):
        return self.rect.collidepoint(*point)


class Menu:
    
    def __init__(self, screen:pygame.Surface|tuple[int,int]) -> None:
        current = Path(__file__).parent
        self.xml_maps_path = current / 'maps'
        self.img_maps_path = current / 'media' / 'minimaps'
        if isinstance(screen, pygame.Surface):
            self.screen_size = screen.get_size()
        elif isinstance(screen, tuple):
            self.screen_size = screen
        else:
            raise TypeError('Параметр screen должен быть tuple, list или pygame.Surface')
        self.quantity_in_row = 4
        self.size = self.screen_size[0], self.screen_size[1] // 2
        self.default_panel_size = self.size[0] // 4
    
    
    def get_data(self, plug):
        data = {}
        xml_maps = list(self.xml_maps_path.iterdir())
        xml_maps = list(filter(lambda x: x.suffix == '.xml', xml_maps))
        img_maps = list(self.img_maps_path.iterdir())
        img_maps = list(filter(lambda x: x.suffix in ['.jpg','.png'], img_maps))
        for x in xml_maps:
            data[x] = plug
            for i in img_maps:
                if x.stem == i.stem:
                    data[x] = i
        self.data = data.copy()
        return data

    
    def __get_x_coords(self, num_row_elems):
        if num_row_elems > self.quantity_in_row:
            raise Exception('Переданое значение nun_row_elems больше Menu.quantity_in_row')
        free_space_row = self.screen_size[0] - self.default_panel_size * num_row_elems
        spaces_size = free_space_row // (num_row_elems + 1)
        coords_x = []
        start = 0
        for i in range(num_row_elems):
            x = start + spaces_size
            coords_x.append(x)
            start += spaces_size + self.default_panel_size
        return coords_x
        
    
    def __is_valid_panel_size(self, num_rows):
        return num_rows * self.default_panel_size + (num_rows+1) * 2 <= self.size[1]
    
    
    def get_positions_maps(self):
        num_minimaps = len(self.data)
        num_rows = num_minimaps // self.quantity_in_row + 1
        maps_img = list(self.data.values())
        while True:
            if self.__is_valid_panel_size(num_rows):
                break
            self.default_panel_size -= 5
        spapces_size = self.size[1] - self.default_panel_size * num_rows
        spapces_size = spapces_size // num_rows+1
        begin = 0
        y = self.size[1] + spapces_size
        coords = []
        for i in range(num_rows):
            coords_x = self.__get_x_coords(self.quantity_in_row)
            coords_y = [y for _ in range(len(coords_x))]
            coords.extend(list(zip(coords_x, coords_y)))
        return coords
    
    
    def create_menu(self, group):
        coords = self.get_positions_maps()
        imgs = list(self.data.values())
        maps = list(self.data.keys())
        for i, (map, img) in enumerate(self.data.items()):
            size=self.default_panel_size, self.default_panel_size
            mm = MiniMap(img, map, size=size, pos=coords[i])
            mm.add(group)





if __name__ == "__main__":
    ...
    menu = Menu((800, 600))
    print(menu.xml_maps_path)
    print(menu.img_maps_path)
    print(menu.get_data(''))

    print(menu.get_positions_maps())
