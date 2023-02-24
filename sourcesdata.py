import pygame
from pathlib import Path

from rich import print

from railway import (
        DecorMapElement, 
        RWArrow, 
        RWStraightSection, 
        RWTurn
)

CURRENT = Path(__file__).parent
MEDIA = CURRENT / 'media'
MMAPS = CURRENT / 'media' / 'minimaps'
MAPS = CURRENT / 'maps'
SOUNDS = CURRENT / 'sounds'

plug = MMAPS / 'plug.jpg'

rwdata = {
    'line_lr': [RWStraightSection, MEDIA / 'line_lr.png'],
    'line_tb': [RWStraightSection, MEDIA / 'line_tb.png'],
    'turn_rb': [RWTurn, MEDIA / 'turn_rb.png'],
    'turn_lb': [RWTurn, MEDIA / 'turn_lb.png'],
    'turn_rt': [RWTurn, MEDIA / 'turn_rt.png'],
    'turn_lt': [RWTurn, MEDIA / 'turn_lt.png'],
    'notprimary1': [DecorMapElement, MEDIA / 'bush2.png'],
    'notprimary2': [DecorMapElement, MEDIA / 'bush3.png'],
    'notprimary3': [DecorMapElement, MEDIA / 'bush1.png'],
    'notprimary4': [DecorMapElement, MEDIA / 'bush4.png'],
    'arrow_rt_rb_tb': [RWArrow, [MEDIA / 'arrow_rt_rb_l.png', MEDIA / 'arrow_rt_rb_r.png']],
    'arrow_lt_lb_tb': [RWArrow, [MEDIA / 'arrow_lt_lb_l.png', MEDIA / 'arrow_lt_lb_r.png']],
    'arrow_lb_rb_lr': [RWArrow, [MEDIA / 'arrow_lb_rb_l.png', MEDIA / 'arrow_lb_rb_r.png']],
    'arrow_lt_rt_lr': [RWArrow, [MEDIA / 'arrow_lt_rt_l.png', MEDIA / 'arrow_lt_rt_r.png']],
} 

loco_left_src = MEDIA / 'loco_left.png'
loco_right_src = MEDIA / 'loco_right.png'
loco_up_src = MEDIA / 'loco_up.png'
loco_down_src = MEDIA / 'loco_down.png'


enemy1_left_src = MEDIA / 'locobluered_left.png'
enemy1_right_src = MEDIA / 'locobluered_right.png'
enemy1_up_src = MEDIA / 'locobluered_up.png'
enemy1_down_src = MEDIA / 'locobluered_down.png'

enemy1_data = [enemy1_left_src, {'right': enemy1_right_src,
                                 'up': enemy1_up_src,
                                 'down': enemy1_down_src,
                                 'speed': 2}]


explosion_data = [
    MEDIA / 'explosion' / 'explosion1.png',
    MEDIA / 'explosion' / 'explosion1.png',
    MEDIA / 'explosion' / 'explosion2.png',
    MEDIA / 'explosion' / 'explosion2.png',
    MEDIA / 'explosion' / 'explosion3.png',
    MEDIA / 'explosion' / 'explosion3.png',
    MEDIA / 'explosion' / 'explosion4.png',
    MEDIA / 'explosion' / 'explosion4.png',
    MEDIA / 'explosion' / 'explosion5.png',
    MEDIA / 'explosion' / 'explosion5.png',
    MEDIA / 'explosion' / 'explosion6.png',
    MEDIA / 'explosion' / 'explosion6.png',
    MEDIA / 'explosion' / 'explosion7.png',
    MEDIA / 'explosion' / 'explosion7.png',
    MEDIA / 'explosion' / 'explosion8.png',
    MEDIA / 'explosion' / 'explosion8.png',
    MEDIA / 'explosion' / 'explosion9.png',
    MEDIA / 'explosion' / 'explosion9.png',
    MEDIA / 'explosion' / 'explosion10.png',
    MEDIA / 'explosion' / 'explosion10.png',
    MEDIA / 'explosion' / 'explosion11.png',
    MEDIA / 'explosion' / 'explosion11.png',
    MEDIA / 'explosion' / 'explosion12.png',
    MEDIA / 'explosion' / 'explosion12.png',
]

lifes_data = [
    MEDIA / 'life' / 'life1.png',
    MEDIA / 'life' / 'life2.png',
    MEDIA / 'life' / 'life3.png',
    MEDIA / 'life' / 'life4.png',
    MEDIA / 'life' / 'life5.png',
]

bullet_bonus_data = [
    MEDIA / 'bullets_bonus' / 'pulya0.png',
    MEDIA / 'bullets_bonus' / 'pulya30.png',
    MEDIA / 'bullets_bonus' / 'pulya60.png',
    MEDIA / 'bullets_bonus' / 'pulya90.png',
    MEDIA / 'bullets_bonus' / 'pulya120.png',
    MEDIA / 'bullets_bonus' / 'pulya150.png',
    MEDIA / 'bullets_bonus' / 'pulya180.png',
    MEDIA / 'bullets_bonus' / 'pulya210.png',
    MEDIA / 'bullets_bonus' / 'pulya240.png',
    MEDIA / 'bullets_bonus' / 'pulya270.png',
    MEDIA / 'bullets_bonus' / 'pulya300.png',
    MEDIA / 'bullets_bonus' / 'pulya330.png',
]

heart_bonus_data = [
    MEDIA / 'heart_bonus' / 'heart1.png',
    MEDIA / 'heart_bonus' / 'heart2.png',
    MEDIA / 'heart_bonus' / 'heart3.png',
    MEDIA / 'heart_bonus' / 'heart4.png',
    MEDIA / 'heart_bonus' / 'heart5.png',
    MEDIA / 'heart_bonus' / 'heart6.png',
    MEDIA / 'heart_bonus' / 'heart7.png',
    MEDIA / 'heart_bonus' / 'heart8.png',
    MEDIA / 'heart_bonus' / 'heart9.png',
    MEDIA / 'heart_bonus' / 'heart10.png',
]

coins_bonus_data = [
    MEDIA / 'coins_bonus' / 'coin1.png',
    MEDIA / 'coins_bonus' / 'coin2.png',
    MEDIA / 'coins_bonus' / 'coin3.png',
    MEDIA / 'coins_bonus' / 'coin4.png',
    MEDIA / 'coins_bonus' / 'coin5.png',
    MEDIA / 'coins_bonus' / 'coin6.png',
    MEDIA / 'coins_bonus' / 'coin7.png',
    MEDIA / 'coins_bonus' / 'coin8.png',
    MEDIA / 'coins_bonus' / 'coin9.png',
    MEDIA / 'coins_bonus' / 'coin10.png',
]

explosion_sound = SOUNDS / 'explosion_sound.ogg'
train_sound = SOUNDS / 'train.ogg'
shot_sound = SOUNDS / 'shot_sound.ogg'
ringing_sound = SOUNDS / 'dzyin2.ogg'

fire_ball = MEDIA / 'fireball1.png'

if __name__ == "__main__":
    ...

    


