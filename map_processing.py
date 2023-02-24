import pathlib
from pathlib import Path
from typing import Union, Tuple
import xml.etree.ElementTree as ET

from rich import inspect, print
import pygame
import cv2

from railway import *


class MapFile:
    def __init__(self, filename):
        self.__filename = filename
        self.__mapsize = None
        self.__mapname = None
        self.__content = None
        self.read()
    
    def read(self) -> list[list[str]]:
        # чтение файла с данными карты и получение шаблона карты из 
        # имен элементов котрые будут на карте
        self.__content = list()
        tree = ET.parse(self.__filename)
        root = tree.getroot()
        
        mapsize = root.find('size').text
        mapname = root.find('mapname').text
        self.__mapsize = self.__get_mapsize_from_str(mapsize)
        self.__mapname = 'map' if not mapname else mapname.strip()
        
        rows = root.findall('row')
        for row in rows:
            contentline = list()
            cols = row.findall('col')
            for col in cols:
                num = self.__get_data_from_tags(col, 'num')
                name = self.__get_data_from_tags(col, 'name')
                num = 0 if num is None else int(num.strip())
                name = 'empty' if name is None else name.strip()
                if num == 0:
                    contentline.append('empty')
                    continue
                tmp = [name] * num
                contentline.extend(tmp)
            self.__content.append(contentline)
        self.__content_align()
        return self.__content
    
    @property
    def map_data(self) -> tuple[tuple[int, int] | None, str | None]:
        return self.__mapsize, self.__mapname
    
    @property
    def content(self) -> list[list[str]] | None:
        return self.__content
    
    def __get_data_from_tags(self, root, child_tag):
        elem = root.find(child_tag)
        if elem is None:
            return
        return elem.text
    
    def __content_align(self):
        # выравнивание шаблона карты. недостающие элементы заполняются  
        # пустыми значениями с именем empty. не достающие строки
        # заполняются списками из empty. если строка(список из имен)
        # больше заданной ширины, то она обрезается до ширины
        width, height = self.__mapsize
        diff = height - len(self.__content)
        # добавление не
        for i in range(diff):
            tmp = ['empty'] * width
            self.__content.append(tmp)
        
        for i, row in enumerate(self.__content):
            if len(row) < width:
                tmp = ['empty'] * (width - len(row))
                self.__content[i].extend(tmp)
            if len(row) > width:
                self.__content[i] = row[:width]
    
    def __get_mapsize_from_str(self, mapsize: str) -> tuple[int, int]:
        # получение размера карты из файла в теге size
        # размер состоит из кол-ва спрайтов в высоту и ширину
        mapsize = mapsize.strip().split(',')
        mapsize = tuple(map(lambda x: int(x.strip()), mapsize))
        if len(mapsize) != 2:
            raise Exception('Ошибка при получении размера карты. в MapFile.__get_mapsize')
        return mapsize

# ======================================================================================
# ======================================================================================
# ======================================================================================

class LoadBG:
    
    def __init__(self, bg_map_file, screen:tuple[int, int] | pygame.Surface):
        # 
        # bg_map_file: файл с изображением фона
        # screen: или размер экрана или Surface. Если tuple, то 
        #         первый элемент ширина, второй высота
        # 
        self.__bg_map_file = bg_map_file
        if isinstance(screen, tuple):
            self.__screen_size = screen
        elif isinstance(screen, pygame.Surface):
            self.__screen_size = screen.get_size()
        else:
            raise TypeError('Screen в LoadMap должен быть tuple илил pygame.Surface')
        self.__bgimage = None
    
    def get_bg_surface(self):
        # возвращает фоновое изображение
        bgimage = pygame.image.load(self.__bg_map_file).convert()
        self.__bgimage = pygame.transform.scale(bgimage, self.__screen_size)
        return self.__bgimage

# ======================================================================================
# ======================================================================================
# ======================================================================================

class ElementsMap:
    
    
    def __init__(self, screen_size: tuple[int, int], 
                 map_size: tuple[int, int], map_data: list[list[str]]):
        # 
        # screen_size: размер surface на котрром будут расположены 
        #              элементы карты. (ширина, высота)
        # map_size: размер карты в секциях по вертикали и горизонтали
        # map_data: список с именнами элементов на карте по строкам
        # в порядке их расположения
        # 
        self.__screen_size = screen_size
        self.__map_size = map_size
        self.__size_sections = self.__get_size_sections()
        self.__map_elements = pygame.sprite.Group()
        self.__content = map_data
        self.__coords = []
        self.__available_coords = []
        self.__centers = []
    
    
    def __get_size_sections(self) -> int:
        # получение размера секции
        num_hor_sections, num_vert_sections = self.__map_size
        screen_width, screen_height = self.__screen_size
        
        dif_screen = screen_width - screen_height
        dif_sections = num_hor_sections - num_vert_sections
        
        if (dif_screen < 0 and dif_sections >= 0) or \
           (dif_screen > 0 and dif_sections <= 0) or \
           (dif_screen == 0 and dif_sections != 0) or \
           (dif_sections == 0 and dif_screen != 0):
            raise Exception("Соотношение сторон экрана не соответствует соотношению сторон карты")
        
        if screen_width >= screen_height:
            sect_size = screen_width // num_hor_sections
            if (sect_size * num_vert_sections - screen_height) > 0:
                sect_size = screen_height // num_vert_sections
            return sect_size
        sect_size = screen_height // num_vert_sections
        if (sect_size * num_hor_sections - screen_width) > 0:
            sect_size = screen_width // num_hor_sections
        return sect_size
    
    
    def get_sections_coords(self) -> tuple[list[int], list[int]]:
        first_coord_width = (self.__screen_size[0] - self.__size_sections * self.__map_size[0]) // 2
        first_coord_height = (self.__screen_size[1] - self.__size_sections * self.__map_size[1]) // 2
        x1 = [first_coord_width]
        y1 = [first_coord_height]
        x2 = [first_coord_width + self.__size_sections]
        y2 = [first_coord_height + self.__size_sections]
        [x1.append(x1[i-1]+self.__size_sections) for i in range(1, self.__map_size[0])]
        [x2.append(x2[i-1]+self.__size_sections) for i in range(1, self.__map_size[0])]
        [y1.append(y1[i-1]+self.__size_sections) for i in range(1, self.__map_size[1])]
        [y2.append(y2[i-1]+self.__size_sections) for i in range(1, self.__map_size[1])]
        xc = list(map(lambda x: x+self.__size_sections//2, x1))
        yc = list(map(lambda x: x+self.__size_sections//2, y1))
        xy1 = []
        xy2 = []
        xyc = []
        for i in range(self.__map_size[1]):
            xy1.extend(list(zip(x1, [y1[i]]*self.__map_size[0])))
            xy2.extend(list(zip(x2, [y2[i]]*self.__map_size[0])))
            xyc.extend(list(zip(xc, [yc[i]]*self.__map_size[0])))
        self.__coords = [xy1, xy2]
        self.__centers = xyc
        return xy1, xy2, xyc
    
    
    
    @property
    def section_size(self):
        return self.__size_sections
    
    
    def create_object(self, CLASS, *args, **kwargs):
        return CLASS(*args, **kwargs)
    
    
    def create_elements(self, data: dict, group):
        # data - {name: [наследник railway.RailWay, [аргументы передающиеся в конструктор], ..., }
        if not self.__coords:
            raise Exception('Не определены координаты элементов карты')
        if not self.__content:
            raise Exception('Нет данных элементов карты.')
        width, height = self.__map_size
        coord_index = 0
        for i in range(height):
            for j in range(width):
                name = self.__content[i][j]
                coords = self.__coords[0][coord_index]
                c = self.__coords[1][coord_index]
                size = c[0] - coords[0], c[1] - coords[1]
                coord_index += 1
                if name == 'empty' or name not in data:
                    continue
                class_, filename = data[name]
                if class_.__name__ == 'RailwayArrow':
                    obj = self.create_object(class_, *filename, name, coords, size)
                elif class_.__name__ == 'RWArrow':
                    left, right = filename[0], filename[1]
                    obj = self.create_object(class_, left, name, right=right, pos=coords, size=size)
                else:
                    # print(name, class_, filename)
                    obj = self.create_object(class_, filename, name, pos=coords, size=size)
                if name in ['line_lr', 'line_tb']:
                    self.__available_coords.append(obj.rect.center)
                obj.add(group)
    
    
    @property
    def available_coords(self):
        return self.__available_coords
    
    
    @property
    def begins(self):
        return self.__coords[0]




if __name__ == "__main__":
    ...
    
    mf = MapFile('land.xml')
    
    map_size, mapname = mf.map_data
    map_content = mf.content
    
    image = cv2.imread('bgimage.png')
    h, w = image.shape[:2]
    elems = ElementsMap((w, h), map_size, map_content)
    sect = elems.section_size
    c1, c2 = elems.get_sections_coords()
    print(c1)
    for i in range(len(c1)):
        cv2.rectangle(image, c1[i], c2[i], (30, 70, 255), 2)
    
    cv2.imshow('image', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    
    
    
    
    
    
    
    
    

