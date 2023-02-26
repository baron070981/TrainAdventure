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
from infoprocess import *
from mtimes import Signal
import explosions

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
enemy_group = pygame.sprite.Group() # группа противников
bonus_group = pygame.sprite.Group() # группа бонусов

# создание меню
menu = Menu(SCREEN_SIZE)
# получение данных о картах в ./media/minimaps и ./maps
menu_data = menu.get_data(sd.plug)
menu.create_menu(menu_group)

mf = MapFile(list(menu_data.keys())[0])
map_size, mapname = mf.map_data
map_content = mf.content

elems = ElementsMap(SCREEN_SIZE, map_size, map_content)
elems.get_sections_coords()

data = sd.rwdata
elems.create_elements(data, rw_group)

# получение списка элементов только прямых участков
straightsections = list(filter(lambda x: x.name in ['line_lr', 'line_tb'], list(rw_group)))

# создание объекта паравозика
loco_left_surf = pygame.image.load(sd.loco_left_src).convert_alpha()
loco_right_surf = pygame.image.load(sd.loco_right_src).convert_alpha()
loco_up_surf = pygame.image.load(sd.loco_up_src).convert_alpha()
loco_down_surf = pygame.image.load(sd.loco_down_src).convert_alpha()
loco_size = elems.section_size - (elems.section_size // 5)
loco = Locomotive(loco_left_surf, right=loco_right_surf, pos=(0,0), size=100,
                  up=loco_up_surf, down=loco_down_surf, decrease=1)

# создание surfce'ов паравозиков-врагов
loco_enemy1_left = pygame.image.load(sd.enemy1_left_src).convert_alpha()
loco_enemy1_right = pygame.image.load(sd.enemy1_right_src).convert_alpha()
loco_enemy1_up = pygame.image.load(sd.enemy1_up_src).convert_alpha()
loco_enemy1_down = pygame.image.load(sd.enemy1_down_src).convert_alpha()

# объект пули
fire_ball = FireBall(sd.fire_ball, (0, 0), (loco_size//4, loco_size//4), RWDirection.DIR_LEFT, speed=8)
fire_ball.start_life_count = 50

# обект взрыва
x_y = elems.section_size + elems.section_size // 2
expl_size = (x_y, x_y)
explosion_surf = explosions.Explosion(expl_size, sd.explosion_data, speed=0.1)

# обект отображающий кол-во жизней
life_size = elems.section_size*5, elems.section_size//2 + elems.section_size//3
loco_life = LocoLifeInfo((10,10), (elems.section_size*4, elems.section_size//2), 5, sd.lifes_data)

# объект отображающий оставшееся кол-во выстрелов
tmp_size = int(elems.section_size / 100 * 55)
bullet_info_size = (tmp_size, tmp_size)
bullet_info = BulletsInfo((SCREEN_SIZE[0]-70, 10), bullet_info_size, str(sd.bullet_bonus_data[0]), 5)

# обект отображающий кол-во собраных монет
coins_info_size = bullet_info_size
coins_info = CoinsInfo((SCREEN_SIZE[0]//2-20, 10), coins_info_size, str(sd.coins_bonus_data[0]), 0)

# 
positions = [e.rect.center for e in straightsections]
random.shuffle(positions)
pos = positions.pop()
bullet_bonus = BaseBonuse('bullet')
bullet_bonus.init_list(sd.bullet_bonus_data,(elems.section_size, elems.section_size), speed=.1)

# 
pos = positions.pop()
heart_bonus = BaseBonuse('heart')
heart_bonus.init_list(sd.heart_bonus_data,(elems.section_size, elems.section_size), speed=.1)

# 
ringing_sound = pygame.mixer.Sound(str(sd.ringing_sound))
shot_sound = pygame.mixer.Sound(str(sd.shot_sound))
explosion_sound = pygame.mixer.Sound(str(sd.explosion_sound))
train_sound = pygame.mixer.Sound(str(sd.train_sound))
train_sound.set_volume(.5)
ch  = train_sound.play(-1)
ch.pause()

BONUS_PLAY = True 
SHOOT = False # флаг разрешающий выстрел(False - можно)
PLAY_SOUND = False # флаг проигрывания фоновой музыки
LOCO_LIFE = True # флаг указывающий, что паравозик не погиб
NUM_ENEMY = 5 # кол-во противников
FLAG = True # флаг позволяющий сменять фоновое мзображение один раз, а не каждую итерацию в игровом цикле
MENU = True # флаг указывающий, что открыто меню
RESET_ARROW_TIMER = Signal(45) # таймер переключения стрелок через 45 сек.
DELAY_ARROW_RESET = Signal(2) # задержка до следующей возможности переключить стрелки
DELAY_ARROW_RESET.start()

clock = pygame.time.Clock()



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
        elif not MENU and keys[pygame.K_r]:
            if DELAY_ARROW_RESET.is_stop():
                DELAY_ARROW_RESET.start()
                for e in rw_group:
                    if isinstance(e, RWArrow):
                        e.reset_turn2()
        # выстрел
        elif not MENU and keys[pygame.K_SPACE] and not SHOOT:
            if loco.bullets > 0: # если у паравозика ести пули
                fire_ball.direct = loco.direct
                # fire_ball.rect.x = loco.rect.x
                # fire_ball.rect.y = loco.rect.y
                fire_ball.rect.center = loco.rect.center
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
                        bonus_group.empty()
                        mf = MapFile(str(panel.mapfile)) # загрузка файла с картой
                        map_size, mapname = mf.map_data
                        map_content = mf.content
                        
                        elems = ElementsMap(SCREEN_SIZE, map_size, map_content)
                        elems.get_sections_coords()
                        elems.create_elements(data, rw_group)
                        
                        explosion_surf.set_attrs(size=elems.section_size + elems.section_size)
                        
                        loco_size = elems.section_size - (elems.section_size // 5)
                        loco.set_attrs(size=loco_size)
                        loco.recovery_life()
                        loco.reload_gun()
                        
                        # список только прямых участков пути
                        straightsections = list(filter(lambda x: x.name in ['line_lr', 'line_tb'], list(rw_group)))
                        rwelems = straightsections.copy()
                        random.shuffle(rwelems)
                        # выбор случайного прямого участка
                        rw_elem = rwelems.pop()
                        pos = rw_elem.rect.center
                        loco.current_pos = pos
                        # размещение паравозика на случайном выбраном участке
                        loco.set_direct(rw_elem.direct)
                        ch.unpause()
                        
                        # создание паравазиков-врагов и размещение их на случайных участках
                        for i in range(NUM_ENEMY):
                            rw_elem = rwelems.pop()
                            pos = rw_elem.rect.center
                            enemy = Locomotive(loco_enemy1_left, right=loco_enemy1_right, 
                                               up=loco_enemy1_up, down=loco_enemy1_down, 
                                               direct=rw_elem.direct, 
                                               pos=pos, size=loco_size, speed=2)
                            enemy.current_pos = pos
                            enemy.set_direct(rw_elem.direct)
                            enemy.add(enemy_group)
                        
                        bullet_bonus.set_attrs(size=elems.section_size-20)
                        bullet_bonus.set_position(rwelems.pop().rect.center)
                        heart_bonus.set_attrs(size=elems.section_size-20)
                        heart_bonus.set_position(rwelems.pop().rect.center)
                        
                        coins = []
                        for i in range(5):
                            coin_bonus = BaseBonuse('coin')
                            coin_bonus.init_list(sd.coins_bonus_data,(elems.section_size//2, elems.section_size//2), speed=.07)
                            coin_bonus.set_position(rwelems.pop().rect.center)
                            coins.append(coin_bonus)
                        
                        bonus_group.add(bullet_bonus)
                        bonus_group.add(heart_bonus)
                        [bonus_group.add(c) for c in coins]
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
            DELAY_ARROW_RESET.stop()
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
                for b in bonus_group:
                    if loco.is_collide(b.rect.center):
                        ringing_sound.play()
                        pos = random.choice(straightsections).rect.center
                        match b.id_name:
                            case 'bullet':
                                bullet_bonus.set_position(pos)
                                loco.reload_gun()
                                bullet_info.set_value(loco.bullets)
                            case 'heart':
                                loco.recovery_life()
                                loco_life.set_life(loco.life)
                                heart_bonus.set_position(pos)
                            case 'coin':
                                b.set_position(pos)
                                loco.coins += 1
                                coins_info.set_value(loco.coins)
            
            
            loco.update()
            screen.blit(loco.image, (loco.rect.x, loco.rect.y))
            enemy_group.draw(screen)
            screen.blit(loco_life.image, (loco_life.rect.x, loco_life.rect.y))
            bullet_info.draw(screen)
            coins_info.draw(screen)
            
            if BONUS_PLAY:
                for bon in bonus_group:
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










