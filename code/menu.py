import pygame as pg
from support import *

class Intro(States):
    def __init__(self):
        States.__init__(self)
        image_path = pg.image.load('graphics/img/titlescreen.png')
        self.introscreen = pg.transform.scale(image_path, (WIDTH, HEIGHT*2))
        self.next = 'menu'

    def cleanup(self):
        print('cleaning up Menu state stuff')

    def startup(self):
        pass

    def get_event(self,event):
        if event.type == pg.KEYDOWN:
            self.done = True
        elif event.type == pg.MOUSEBUTTONDOWN:
            self.done = True

    def update(self,screen,dt):
        self.draw(screen)

    def draw(self, screen):
        screen.fill((0,0,0))
        screen.blit(self.introscreen,(0,0))
        Text(screen,(WIDTH/2,HEIGHT-2*TILESIZE),'Press any key to continue',FONT,40,black)

class MenuManager:
    def __init__(self):
        self.selected_index = 0
        self.last_option = None
        self.selected_image = get_sprite(0,TILESIZE*1.5,TILESIZE*4,TILESIZE,ss_ui)
        self.deselected_image = (255,255,255)

class Menu(States):
    def __init__(self):
        States.__init__(self)
        image = pg.image.load('graphics/img/menu_background.png')
        self.bg = pg.transform.scale(image,(RESOLUTION))
        self.next = 'game'

    def cleanup(self):
        print('cleaning up Menu state stuff')

    def startup(self):
        print('starting Menu state stuff')

    def get_event(self,event):
        if event.type == pg.KEYDOWN:
            print('Menu State keydown')
        elif event.type == pg.MOUSEBUTTONDOWN:
            self.done = True

    def update(self,screen,dt):
        self.draw(screen)

    def draw(self,screen):
        screen.fill((0,0,0))
        screen.blit(self.bg,(0,0))
        Button(screen,(100,100))