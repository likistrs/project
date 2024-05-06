# команда для сборки игры в один исходный файл
# pyinstaller --onefile --name MyGame --icon=icon.ico -F --noconsole main5.py

import pygame as PG
import sys
from random import randint
PG.init()

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 700
SCREEN = PG.display.set_mode( (SCREEN_WIDTH, SCREEN_HEIGHT) )
FPS = 60
CLOCK = PG.time.Clock()

#PG.mouse.set_visible(False)

PG.mixer.init()

sound_hit_1 = PG.mixer.Sound('./src/sounds/se_hit.mp3')

PG.mixer.music.load('./src/music/bgm_space_4.mp3')
PG.mixer.music.set_volume(0.7)
PG.mixer.music.play()

bg_image = PG.image.load('./src/images/space_bg_tile_1524x802px.jpg')
#bg_image = PG.transform.scale( bg_image, (960, 701) )
bg_draw_point = (0, 0)

ball_image = PG.image.load('./src/images/ball_116x116px.png')
ball_image = PG.transform.scale( ball_image, (32, 32) )

player_left_image = PG.image.load('./src/images/p1_128x512px.png')
player_left_image = PG.transform.scale( player_left_image, (32, 128) )

player_right_image = PG.image.load('./src/images/p2_128x512px.png')
player_right_image = PG.transform.scale( player_right_image, (32, 128) )

class Label():
    def __init__(self, text, x, y, align = 'left', font_size = 36, color = (255, 255, 255)):
        self.font = PG.font.Font(None, font_size)
        self.align = align
        self.color = color
        self.x = x
        self.y = y
        self.render(text)
    
    def render(self, text):
        self.text = self.font.render(text, True, self.color)
        self.rect = self.text.get_rect()
        self.rect.centery = self.y
        if self.align == 'left': self.rect.left = self.x
        elif self.align == 'right': self.rect.right = self.x
        else : self.rect.centerx = self.x

class Ball(PG.sprite.Sprite):
    def __init__(self):
        PG.sprite.Sprite.__init__(self)
        self.image = ball_image
        self.rect = self.image.get_rect()
        self.speed = 5
        self.restart()
    
    def restart(self):
        self.rect.centerx = SCREEN_WIDTH * 0.5
        self.rect.centery = SCREEN_HEIGHT * 0.5
        self.speed_x = self.speed if randint(0,1) == 1 else -self.speed
        self.speed_y = self.speed if randint(0,1) == 1 else -self.speed

    def update(self):
        self.rect.x += self.speed_x 
        self.rect.y += self.speed_y 
        if self.rect.top < 0:
            self.rect.top = 0
            self.speed_y *= -1
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
            self.speed_y *= -1
        if self.rect.colliderect(p_left.rect):
            self.rect.left = p_left.rect.right
            self.speed_x *= -1
        if self.rect.colliderect(p_right.rect):
            self.rect.right = p_right.rect.left
            self.speed_x *= -1
        if self.rect.left < 0:
            p_right.score += 1
            p_right.score_label.render(f'Score: {p_right.score}')
            self.restart()
        if self.rect.right > SCREEN_WIDTH:
            p_left.score += 1
            p_left.score_label.render(f'Score: {p_left.score}')
            self.restart()

        SCREEN.blit(self.image, self.rect)

class Player_left(PG.sprite.Sprite):
    def __init__(self):
        PG.sprite.Sprite.__init__(self)
        self.image = player_left_image
        self.rect = self.image.get_rect()
        self.speed = 5
        self.rect.left = 0
        self.rect.centery = SCREEN_HEIGHT * 0.5
        self.score = 0
        self.score_label = Label(f'Score: {self.score}', 15, 30, 'left', 36, (0, 255, 255))

    def update(self):
        KEY = PG.key.get_pressed()
        if KEY[PG.K_w]:
            self.rect.y -= self.speed
            if self.rect.y < 0 : self.rect.y = 0
        elif KEY[PG.K_s]:
            self.rect.y += self.speed
            if self.rect.bottom > SCREEN_HEIGHT : self.rect.bottom = SCREEN_HEIGHT

        SCREEN.blit(self.image, self.rect)
        SCREEN.blit(self.score_label.text, self.score_label.rect)

class Player_right(PG.sprite.Sprite):
    def __init__(self):
        PG.sprite.Sprite.__init__(self)
        self.image = player_right_image
        self.rect = self.image.get_rect()
        self.speed = 5
        self.rect.right = SCREEN_WIDTH
        self.rect.centery = SCREEN_HEIGHT * 0.5
        self.score = 0
        self.score_label = Label(f'Score: {self.score}', SCREEN_WIDTH - 15, 30, 'right', 36, (255, 0, 255))

    def update(self):
        KEY = PG.key.get_pressed()
        if KEY[PG.K_UP]:
            self.rect.y -= self.speed
            if self.rect.y < 0 : self.rect.y = 0
        elif KEY[PG.K_DOWN]:
            self.rect.y += self.speed
            if self.rect.bottom > SCREEN_HEIGHT : self.rect.bottom = SCREEN_HEIGHT
        SCREEN.blit(self.image, self.rect)
        SCREEN.blit(self.score_label.text, self.score_label.rect)

 
p_left = Player_left()
p_right = Player_right()
ball = Ball()

tick = 0 # создаем счетчик кадров
game_loop_is = True

# ГЛАВНыЙ ЦИКЛ ИГРЫ
while game_loop_is:
    CLOCK.tick(FPS)
    tick += 1

    for event in PG.event.get():
        if event.type == PG.QUIT or (event.type == PG.KEYDOWN and event.key == PG.K_ESCAPE):
            game_loop_is = False

    SCREEN.blit(bg_image, bg_draw_point)
    p_left.update()
    p_right.update()
    ball.update()

    PG.display.flip()

PG.quit()
sys.exit()