import pygame as pg
import time
from support import *

class Titlescreen(States):
    def __init__(self):
        States.__init__(self)
        image_path = pg.image.load('graphics/img/titlescreen.png')
        self.introscreen = pg.transform.scale(image_path, (WIDTH, HEIGHT*2))
        self.next = 'menu'

    def cleanup(self):
        print('nothing to clean')

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
        Text(screen,(WIDTH / 2, HEIGHT - 2 * TILESIZE),'Press any key to continue',FONT,40,black)

class MenuManager():
    def __init__(self):
        self.selected_index = 0
        self.last_option = None
        self.selected_color = (255,255,0)
        self.deselected_color = (255,255,254)
        self.from_bottom = TILESIZE
        self.spacer = TILESIZE * 1.5

    def draw_menu(self, screen):
        for i,opt in enumerate(self.rendered["des"]):
            opt[2].center = (200,self.from_bottom + i * self.spacer)
            opt[3].center = (200,self.from_bottom + i * self.spacer)
            if i == self.selected_index:
                rend_img,rend_txt,rend_rect,rend_rect_txt = self.rendered["sel"][i]
                rend_rect.center = opt[2].center
                rend_rect_txt.center = opt[3].center
                screen.blit(rend_img,rend_rect)
                screen.blit(rend_txt,rend_rect_txt)
            else:
                screen.blit(opt[0],opt[2])
                screen.blit(opt[1],opt[3])


    def update_menu(self):
        self.change_selected_option()

    def get_event_menu(self,event):
        if event.type == pg.KEYDOWN:
            if event.key in [pg.K_UP]:
               self.change_selected_option(-1)
            elif event.key in [pg.K_DOWN]:
               self.change_selected_option(1)
            elif event.key == pg.K_RETURN:
               self.select_option(self.selected_index)
        self.mouse_menu_click(event)

    def mouse_menu_click(self, event):
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            for i,opt in enumerate(self.rendered["des"]):
                if opt[2].collidepoint(pg.mouse.get_pos()):
                    self.selected_index = i
                    self.select_option(i)
                    break       
    def pre_render_options(self):
        font_deselect = pg.font.SysFont(FONT, 30)
        font_selected = pg.font.SysFont(FONT, 35)

        rendered_msg = {"des":[],"sel":[]}
        for option in self.options:
            d_img  = get_sprite(0,TILESIZE*2.5,TILESIZE*4,TILESIZE,ss_ui)
            d_txt = font_deselect.render(option, 1, self.deselected_color)
            d_rect = d_img.get_rect()
            d_rect_txt = d_txt.get_rect()
            s_img = get_sprite(0,TILESIZE*1.5,TILESIZE*4,TILESIZE,ss_ui)
            s_txt = font_selected.render(option, 1, self.selected_color)
            s_rect = s_img.get_rect()
            s_rect_txt = s_txt.get_rect()
            rendered_msg["des"].append((d_img,d_txt,d_rect,d_rect_txt))
            rendered_msg["sel"].append((s_img,s_txt,s_rect,s_rect_txt))
        self.rendered = rendered_msg

    def select_option(self,i):
        if i == len(self.next_list[i]):
            self.quit = True
        else:
            self.next = self.next_list[i]
            self.done = True
            self.selected_index = 0

    def change_selected_option(self,op=0):
        for i,opt in enumerate(self.rendered["des"]):
            if opt[2].collidepoint(pg.mouse.get_pos()):
                self.selected_index = i
        
        if op:
            self.selected_index += op
            max_i = len(self.rendered["des"]) - 1
            if self.selected_index < 0:
                self.selected_index = max_i
            elif self.selected_index > max_i:
                self.selected_index =0

class Menu(States,MenuManager):
    def __init__(self):
        States.__init__(self)
        MenuManager.__init__(self)
        image = pg.image.load('graphics/img/menu_background.png')
        self.bg = pg.transform.scale(image,(RESOLUTION))
        self.next = 'game'
        self.options = ['New Game', 'Options','Quit']
        self.next_list = ['game','options','quit']
        self.pre_render_options()

    def cleanup(self):
        print('cleaning up Menu state stuff')

    def startup(self):
        print('starting Menu state stuff')

    def get_event(self,event):
        if event.type == pg.QUIT:
                self.quit = True
        self.get_event_menu(event)

    def update(self,screen,dt):
        self.update_menu()
        self.draw(screen)

    def draw(self,screen):
        screen.fill((0,0,0))
        screen.blit(self.bg,(0,0))
        self.draw_menu(screen)

class Options(States,MenuManager):
    def __init__(self):
        States.__init__(self)
        MenuManager.__init__(self)
        image = pg.image.load('graphics/img/menu_background.png')
        self.bg = pg.transform.scale(image,(RESOLUTION))
        self.next = 'game'
        self.options = ['Grafics','Sounds','Menu']
        self.next_list = ['game','game','menu']
        self.pre_render_options()

    def cleanup(self):
        print('cleaning up Menu state stuff')

    def startup(self):
        print('starting Options state stuff')

    def get_event(self,event):
        if event.type == pg.KEYDOWN:
            print('Menu State keydown')
        elif event.type == pg.MOUSEBUTTONDOWN:
            self.done = True
        self.get_event_menu(event)

    def update(self,screen,dt):
        self.update_menu()
        self.draw(screen)

    def draw(self,screen):
        screen.fill((0,0,0))
        screen.blit(self.bg,(0,0))
        self.draw_menu(screen)

class Quit(States):
    def __init__(self):
        States.__init__(self)
        image = pg.image.load('graphics/img/menu_background.png')
        self.bg = pg.transform.scale(image,(RESOLUTION))

    def cleanup(self):
        print('start Quitting the game')

    def startup(self):
        print('Quit')

    def get_event(self,event):
        pass

    def update(self,screen,dt):
        self.draw(screen)

    def draw(self,screen):
        screen.fill((0,0,0))
        screen.blit(self.bg,(0,0))

class Intro(States):
    def __init__(self):
        States.__init__(self)
        image = pg.image.load('graphics/img/menu_background.png')
        self.bg = pg.transform.scale(image,(RESOLUTION))

    def cleanup(self):
        print('start Quitting the game')

    def startup(self):
        print('play Intro')

    def get_event(self,event):
        pass

    def update(self,screen,dt):
        self.draw(screen)

    def draw(self,screen):
        screen.fill((0,0,0))
        screen.blit(self.bg,(0,0))
