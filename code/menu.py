import pygame as pg
from support import *

class Intro(States):
    def __init__(self):
        States.__init__(self)
        image_path = pg.image.load('graphics/img/titlescreen.png')
        self.titlescreen = pg.transform.scale(image_path, (WIDTH, HEIGHT*2))
        self.font = pg.font.Font('graphics/font/Pixel.ttf', 32)
        self.next = 'menu'
        self.pos = 0

    def cleanup(self):
        print('cleaning up Menu state stuff')

    def startup(self):

        while self.done == False:
            i = 0
            if i == HEIGHT:
                self.screen.blit(self.titlescreen,(0,HEIGHT))
                i = HEIGHT - 5
            i += 5
            self.pos = i
            return self.pos

    def get_event(self, event):
        if event.type == pg.KEYDOWN:
            self.done = True
        elif event.type == pg.MOUSEBUTTONDOWN:
            self.done = True

    def update(self, screen, dt):
        self.draw(screen)

    def draw(self, screen):
        screen.fill((0,0,0))
        screen.blit(self.titlescreen,(0,-self.pos))
        title = self.font.render('Press any key to continue', True, black)
        title_rect = title.get_rect(x=TILESIZE, y=300)
        screen.blit(title,title_rect)

class Menu(States):
    def __init__(self):
        States.__init__(self)
        self.next = 'game'

    def cleanup(self):
        print('cleaning up Menu state stuff')

    def startup(self):
        print('starting Menu state stuff')

    def get_event(self, event):
        if event.type == pg.KEYDOWN:
            print('Menu State keydown')
        elif event.type == pg.MOUSEBUTTONDOWN:
            self.done = True

    def update(self, screen, dt):
        self.draw(screen)

    def draw(self, screen):
        screen.fill((0,255,0))