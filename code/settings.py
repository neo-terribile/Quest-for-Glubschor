from ctypes.wintypes import RGB

import pygame as pg

CAPTION = "Quest for Glubschor"
WIDTH    = 1920	
HEIGHT   = 1080
RESOLUTION = (WIDTH, HEIGHT)
FPS      = 60
TILESIZE = 64

pg.init()

SCREEN = pg.display.set_mode(RESOLUTION)
SCREEN_RECT = SCREEN.get_rect()

#spritesheets
ss_ui = 'graphics/player/ui.png'
ss_player = 'graphics/player/player.png'


# ui 
BAR_HEIGHT = TILESIZE / 2 - 8
BAR_WIDTH = TILESIZE * 4 - 6
ITEM_BOX_SIZE = 80
UI_FONT = 'graphics/font/joystix.ttf'
UI_FONT_SIZE = 18


# general colors
WATER_COLOR = '#71ddee'
UI_BG_COLOR = '#222222'
UI_BORDER_COLOR = '#111111'
TEXT_COLOR = '#EEEEEE'
black = RGB(0,0,0)
white = RGB(255,255,255)
green = RGB(0,255,0)

# ui colors
HEALTH_COLOR = 'red'
ENERGY_COLOR = 'blue'
UI_BORDER_COLOR_ACTIVE = 'gold'


# weapons 
weapon_data = {
	'sword': {'cooldown': 100, 'damage': 15,'graphic':'graphics/weapons/sword/full.png'}}

# magic
magic_data = {
	'flame': {'strength': 5,'cost': 20,'graphic':'graphics/particles/flame/fire.png'},
	'heal' : {'strength': 20,'cost': 10,'graphic':'graphics/particles/heal/heal.png'}}
