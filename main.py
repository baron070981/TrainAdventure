import pygame
import sys
import random
import time

from rich import print, inspect

from map_processing import LoadBG, MapFile, ElementsMap
from railway import *
from train import *
from menu import *
from bonuses import *
import sourcesdata as sd
from explosions import Explosion
from infoprocess import *
from mtimes import Signal

pygame.init()



FPS = 30

# экран
dispinfo = pygame.display.Info()
SCREEN_SIZE = (dispinfo.current_w-15, dispinfo.current_h-15)
screen = pygame.display.set_mode((SCREEN_SIZE), pygame.DOUBLEBUF | pygame.RESIZABLE | pygame.NOFRAME)

# загрузка фонов
lmap = LoadBG(sd.MEDIA / 'bgimagegreen.png', screen)
lmenu = LoadBG(sd.MEDIA / 'locobg1.png', screen)
bgimage = lmap.get_bg_surface()
menubg = lmenu.get_bg_surface()

main_bg = bgimage.copy() # текущий фон

rw_group = pygame.sprite.Group() # группа для жд путей
menu_group = pygame.sprite.Group() # группа мимникарт в меню
enemy_group = pygame.sprite.Group()

# создание меню
menu = Menu(SCREEN_SIZE)
# получение данных о картах в ./media/minimaps и ./maps
menu_data = menu.get_data(sd.plug)
menu.create_menu(menu_group)


mf = MapFile(sd.MAPS / 'land.xml')
map_size, mapname = mf.map_data
map_content = mf.content

elems = ElementsMap(SCREEN_SIZE, map_size, map_content)
elems.get_sections_coords()

data = sd.rwdata
elems.create_elements(data, rw_group)


straightsections = list(filter(lambda x: x.name in ['line_lr', 'line_tb'], list(rw_group)))
rw_elem = random.choice(straightsections)
pos = rw_elem.rect.center


loco_left_surf = pygame.image.load(sd.loco_left_src).convert_alpha()
loco_right_surf = pygame.image.load(sd.loco_right_src).convert_alpha()
loco_up_surf = pygame.image.load(sd.loco_up_src).convert_alpha()
loco_down_surf = pygame.image.load(sd.loco_down_src).convert_alpha()
loco_size = elems.section_size - (elems.section_size // 5)
loco = Locomotive(pos, loco_size, loco_left_surf, right=loco_right_surf, 
                  up=loco_up_surf, down=loco_down_surf, 
                  direct=rw_elem.direct, decrease=1)


rw_elem = random.choice(straightsections)
pos = rw_elem.rect.center
loco_enemy1_left = pygame.image.load(sd.enemy1_left_src).convert_alpha()
loco_enemy1_right = pygame.image.load(sd.enemy1_right_src).convert_alpha()
loco_enemy1_up = pygame.image.load(sd.enemy1_up_src).convert_alpha()
loco_enemy1_down = pygame.image.load(sd.enemy1_down_src).convert_alpha()
loco_enemy1_size = elems.section_size - (elems.section_size // 5)
loco_enemy1 = Locomotive(pos, loco_enemy1_size, loco_enemy1_left, right=loco_enemy1_right, 
                         up=loco_enemy1_up, down=loco_enemy1_down, direct=rw_elem.direct)


fire_ball = FireBall(sd.fire_ball, (300,300), (loco_size//2, loco_size//2), RWDirection.DIR_LEFT, speed=8)
fire_ball.start_life_count = 50

x_y = elems.section_size + elems.section_size // 2
expl_size = (x_y, x_y)
explosion_surf = Explosion(expl_size, sd.explosion_data)

life_size = elems.section_size*5, elems.section_size//2 + elems.section_size//3
loco_life = LocoLifeInfo((10,10), (elems.section_size*4, elems.section_size//2), 5, sd.lifes_data)

bullet_info_size = (elems.section_size // 3, elems.section_size // 3)
bullet_info = BulletsInfo((SCREEN_SIZE[0]-70, 20), bullet_info_size, str(sd.bullet_bonus_data[0]), 5)


rw_elem = random.choice(straightsections)
positions = [e.rect.center for e in straightsections]
random.shuffle(positions)
pos = positions.pop()
# bullet = BaseBonuse(speed_anim=4, idn='bullet')
bullet = BaseBonuse('bullet')
bullet.init_list(sd.bullet_bonus_data,(elems.section_size, elems.section_size), speed=.1)
bullet.set_position(pos)

pos = positions.pop()
heart = BaseBonuse('heart')
heart.init_list(sd.heart_bonus_data,(elems.section_size, elems.section_size), speed=.1)
heart.set_position(pos)

coins = []
coins_pos = positions.copy()
for i in range(5):
    pos = coins_pos.pop()
    coin = BaseBonuse('coin')
    coin.init_list(sd.coins_bonus_data,(elems.section_size, elems.section_size), speed=.07)
    coin.set_position(pos)
    coins.append(coin)

bonuse_group = pygame.sprite.Group()
bonuse_group.add(bullet)
bonuse_group.add(heart)
[bonuse_group.add(c) for c in coins]

ringing_sound = pygame.mixer.Sound(str(sd.ringing_sound))
shot_sound = pygame.mixer.Sound(str(sd.shot_sound))
explosion_sound = pygame.mixer.Sound(str(sd.explosion_sound))
train_sound = pygame.mixer.Sound(str(sd.train_sound))
train_sound.set_volume(.5)
ch  = train_sound.play(-1)
ch.pause()

BONUS_PLAY = True
SHOOT = False
PLAY_SOUND = False
LOCO_LIFE = True
NUM_ENEMY = 5
FLAG = True
MENU = True
PAUSE = False
RESET_ARROW = 1000
COUNT_BONUS = 300
mouse_pos = None
clock = pygame.time.Clock()

RESET_ARROW_TIMER = Signal(15)

# ====================================================================
# =======================  ИГРОВОЙ ЦИКЛ  =============================
# ====================================================================

if __name__ == "__main__":
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
        keys = pygame.key.get_pressed()
        # вызов меню
        if keys[pygame.K_m]:
            MENU = True
            FLAG = True
            ch.pause() # постановка фонового звука игры на паузу
        # возврат из меню в игру
        elif keys[pygame.K_RETURN]:
            MENU = False
            FLAG = True
            ch.unpause() # снятие фонового звука игры с паузы
        # выстрел
        elif keys[pygame.K_SPACE] and not SHOOT:
            if loco.bullets > 0: # если у паравозика ести пули
                fire_ball.direct = loco.direct
                fire_ball.rect.x = loco.rect.x
                fire_ball.rect.y = loco.rect.y
                loco.shoot() # убавление кол-ва пуль у паравозика
                shot_sound.play()
                SHOOT = True # флаг того, что выстрел произведен и пока он не сменится второй выстрел не произвести
        
        pressed = pygame.mouse.get_pressed()
        # если нажата левая кнопка мыши
        if pressed[0]:
            pos = pygame.mouse.get_pos() # позиция курсора
            if MENU: # если открыто главное меню
                # проход группе с миникартами
                for panel in menu_group:
                    # проверка что позиция курсора совпадает с выбранной картой
                    if panel.is_collide(pos):
                        rw_group.empty() # очистка группы с элементами жд путей и другими элементами карты
                        enemy_group.empty() # очистка группы паравозиков-врагов
                        mf = MapFile(str(panel.mapfile)) # загрузка файла с картой
                        map_size, mapname = mf.map_data
                        map_content = mf.content
                        
                        elems = ElementsMap(SCREEN_SIZE, map_size, map_content)
                        elems.get_sections_coords()
                        elems.create_elements(data, rw_group)
                        
                        # список только прямых участков пути
                        straightsections = list(filter(lambda x: x.name in ['line_lr', 'line_tb'], list(rw_group)))
                        # выбор случайного прямого участка
                        rw_elem = random.choice(straightsections)
                        pos = rw_elem.rect.center
                        loco.current_pos = pos
                        # размещение паравозика на случайном выбраном участке
                        loco.set_direct(rw_elem.direct)
                        ch.unpause()
                        
                        # создание паравазиков-врагов и размещение их на случайных участках
                        for i in range(NUM_ENEMY):
                            rw_elem = random.choice(straightsections)
                            pos = rw_elem.rect.center
                            enemy = Locomotive(pos, loco_size, 
                                               loco_enemy1_left, right=loco_enemy1_right, 
                                               up=loco_enemy1_up, down=loco_enemy1_down, 
                                               direct=rw_elem.direct, speed=2)
                            enemy.current_pos = pos
                            enemy.set_direct(rw_elem.direct)
                            enemy.add(enemy_group)
                        MENU = False
                        FLAG = False
                        main_bg = bgimage.copy()
            else: # если идет игровой цикл
                for e in rw_group:
                    # если курсор совпадает со жд стрелкой
                    if isinstance(e, RWArrow):
                        if e.is_collide(pos):
                            # стрелка переключается
                            e.reset_turn()
        
        # если была нажата кнопка M (выход в главное меню)
        if MENU and FLAG:
            # смена фона
            main_bg = menubg.copy()
            FLAG = False # для того чтоб этот участок отработал один раз после нажатия
        
        # если была нажата клавиша Enter (возврат из меню в начатую игру)
        elif not MENU and FLAG:
            # смена фона
            main_bg = bgimage.copy()
            FLAG = False # для того чтоб этот участок отработал один раз после нажатия
        
        
        
        screen.blit(main_bg, (0,0))
        
        if MENU:
            # отрисовка миникарт
            menu_group.draw(screen)
        
        if not LOCO_LIFE:
            # если паравозик погиб
            MENU = True
            FLAG = True
            LOCO_LIFE = True
            explosion_surf.start = False
            loco.life = 5
            time.sleep(.6)
            ch.pause()
        
        elif not MENU and LOCO_LIFE:
            RESET_ARROW_TIMER.start()
            rw_group.update()
            rw_group.draw(screen)
            
            for e in rw_group:
                # проверка на каком участке находится паравозик
                if e.is_collide(loco.rect.center):
                    if isinstance(e, (RWArrow, RWStraightSection, RWTurn)):
                        # получение новой позиции паравозика из участка на котором он находится
                        x, y, d = e.move(*loco.rect.center, loco.direct, speed=loco.speed)
                    # премещение паравозика согласно полченным координатам x и y
                    # и смена изображения если сменилось напрвление d
                    loco.move(x, y, elems.section_size, d)
                
                # передвижение противников и проверка на столкновение с ними
                for enemy in enemy_group:
                    if e.is_collide(enemy.rect.center):
                        if isinstance(e, (RWArrow, RWStraightSection, RWTurn)):
                            x, y, d = e.move(*enemy.rect.center, enemy.direct, speed=enemy.speed)
                        enemy.move(x, y, elems.section_size, d)
                    
                    # проверка столкновения паравозика с одним из паравозиков-врагов
                    if enemy.is_collide(loco.rect.center):
                        loco.decrease_life() # убавление жизни у паравозика
                        loco_life.set_life(loco.life) # смена изображения с кол-вом сердечек равным оставшимся жизням
                        LOCO_LIFE = loco.is_live() # установка флага жив или нет паравозик
                        explosion_surf.start = True # запуск анимации взрыва
                        explosion_surf.set_position(enemy.rect.center) # установка позиции взрыва равной месту столкновения
                        rw_elem = random.choice(straightsections) # выбор случайного участка пути
                        pos = rw_elem.rect.center 
                        enemy.current_pos = pos # размещение паравозика-врага на случайном участке
                        enemy.set_direct(rw_elem.direct) # установка направления
                        explosion_sound.play() # звук взрыва
                    
                    # проверка попадания пули в паравозика-врага
                    if enemy.is_collide(fire_ball.rect.center):
                        fire_ball.is_live = False
                        explosion_surf.start = True
                        explosion_surf.set_position(enemy.rect.center)
                        rw_elem = random.choice(straightsections)
                        pos = rw_elem.rect.center
                        enemy.current_pos = pos
                        enemy.set_direct(rw_elem.direct)
                        explosion_sound.play()
                        SHOOT = False # смена флага, на разрешающий произвести следующий выстрел
                        fire_ball.reset()
                
                # проверка что элемент жд стрелка и переключение стрелки
                RESET_ARROW_TIMER.stop()
                if isinstance(e, RWArrow) and RESET_ARROW_TIMER.is_stop():
                    e.reset_turn()
            
            if BONUS_PLAY:
                for b in bonuse_group:
                    if loco.is_collide(b.rect.center):
                        ringing_sound.play()
                        match b.id_name:
                            case 'bullet':
                                pos = random.choice(straightsections).rect.center
                                bullet.set_position(pos)
                                loco.reload_gun()
                                bullet_info.set_value(loco.bullets)
                            case 'heart':
                                loco.recovery_life()
                                loco_life.set_life(loco.life)
            
            
            loco.update()
            screen.blit(loco.image, (loco.rect.x, loco.rect.y))
            enemy_group.draw(screen)
            screen.blit(loco_life.image, (loco_life.rect.x, loco_life.rect.y))
            bullet_info.draw(screen)
            
            if BONUS_PLAY:
                for bon in bonuse_group:
                    screen.blit(bon.image, (bon.rect.x, bon.rect.y))
                    bon.iter_surfs()
            
            # если произведен выстрел
            if SHOOT:
                # перемещение пули и убавление внутреннего счетчика жизни пули
                fire_ball.move(loco.speed)
                screen.blit(fire_ball.image, (fire_ball.rect.x, fire_ball.rect.y))
                # отрисовка на экране сколько пуль осталось
                bullet_info.set_value(loco.bullets)
                # если счетчик жизни пули обнулился
                if not fire_ball.is_life_count:
                    SHOOT = False # разрешение на следующий выстрел
                    fire_ball.reset() # сброс координат пули
            
            if explosion_surf.start:
                # отрисовка анимации взрыва
                screen.blit(explosion_surf.image, explosion_surf.rect)
                explosion_surf.iter_surface()
            
        pygame.display.flip()
        pygame.display.update()
        clock.tick(FPS)










