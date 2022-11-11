import pygame as pg
from settings import * 
from support import *


class UI:
	def __init__(self):
		
		# general 
		self.screen = pg.display.get_surface()
		self.font = pg.font.Font(UI_FONT,UI_FONT_SIZE)
		self.sheet = pg.image.load(ss_ui).convert_alpha()
		self.bg = get_sprite(0,0,256, 32,ss_ui)


		# convert weapon dictionary
		self.weapon_graphics = []
		for weapon in weapon_data.values():
			path = weapon['graphic']
			weapon = pg.image.load(path).convert_alpha()
			self.weapon_graphics.append(weapon)

		# convert magic dictionary
		self.magic_graphics = []
		for magic in magic_data.values():
			magic = pg.image.load(magic['graphic']).convert_alpha()
			self.magic_graphics.append(magic)

	#show bar
	def show_bars(self,current,ammount,x,y,dx,dy):

		# converting stat to pixel 
		ratio = current / ammount
		width = BAR_WIDTH * ratio
		bar = pg.Surface([width, BAR_HEIGHT])
		bar.blit(self.sheet, (0, 0), (x, y, width, BAR_HEIGHT))
		bar.set_colorkey('black')

		# drawing the bar
		self.screen.blit(self.bg,(dx, dy))
		self.screen.blit(bar,(dx + 3, dy + 4))
 
	#show exp
	def show_exp(self,exp):
		text_surf = self.font.render(str(int(exp)),False,TEXT_COLOR)
		x = self.screen.get_size()[0] - 20
		y = self.screen.get_size()[1] - 20
		text_rect = text_surf.get_rect(bottomright = (x,y))

		pg.draw.rect(self.screen,UI_BG_COLOR,text_rect.inflate(20,20))
		self.screen.blit(text_surf,text_rect)
		pg.draw.rect(self.screen,UI_BORDER_COLOR,text_rect.inflate(20,20),3)

	def selection_box(self,left,top, has_switched):
		bg_rect = pg.Rect(left,top,ITEM_BOX_SIZE,ITEM_BOX_SIZE)
		pg.draw.rect(self.screen,UI_BG_COLOR,bg_rect)
		if has_switched:
			pg.draw.rect(self.screen,UI_BORDER_COLOR_ACTIVE,bg_rect,3)
		else:
			pg.draw.rect(self.screen,UI_BORDER_COLOR,bg_rect,3)
		return bg_rect

	def weapon_overlay(self,weapon_index,has_switched):
		bg_rect = self.selection_box(10,630,has_switched)
		weapon_surf = self.weapon_graphics[weapon_index]
		weapon_rect = weapon_surf.get_rect(center = bg_rect.center)

		self.screen.blit(weapon_surf,weapon_rect)

	def magic_overlay(self,magic_index,has_switched):
		bg_rect = self.selection_box(80,635,has_switched)
		magic_surf = self.magic_graphics[magic_index]
		magic_rect = magic_surf.get_rect(center = bg_rect.center)

		self.screen.blit(magic_surf,magic_rect)
	
		# display ui
	def draw(self,player):
		self.show_bars(player.health,player.max_health,3,36,10,10)
		self.show_bars(player.energy,player.max_energy,3,68,10,52)

		self.show_exp(player.exp)

		self.weapon_overlay(player.weapon_index,not player.can_switch_weapon)
		self.magic_overlay(player.magic_index,not player.can_switch_magic)