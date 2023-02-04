import pygame as pg
from settings import *
from csv import reader
from os import walk

# import csv
def import_csv_layout(path):
	terrain_map = []
	with open(path) as level_map:
		layout = reader(level_map,delimiter = ',')
		for row in layout:
			terrain_map.append(list(row))
		return terrain_map

# import folder
def import_folder(path):
	surface_list = []

	for _,__,img_files in walk(path):
		for image in img_files:
			full_path = path + '/' + image
			image_surf = pg.image.load(full_path).convert_alpha()
			surface_list.append(image_surf)

	return surface_list

# import animations
def import_animations(sheet,width,height,frames,j):
	surface_list = []
	i = 0
	while i <= frames:
			sprite = pg.Surface([width, height])
			sprite.blit(sheet, (0,0), (width *i, height * j, width, height))
			sprite.set_colorkey(black)  # sprite_background off
			surface_list.append(sprite)
			i += 1
	return surface_list
	
# get sprite
def get_sprite(x,y,width,height,path):
	sheet = pg.image.load(path).convert_alpha() 
	sprite = pg.Surface([width, height])
	sprite.blit(sheet,(0,0), (x, y, width, height))
	sprite.set_colorkey(black)  # sprite_background off
	return sprite

class States(object):
    def __init__(self):
        self.done = False
        self.next = None
        self.quit = False
        self.previous = None
        self.screen_rect = SCREEN_RECT

class YSortCameraGroup(pg.sprite.Group):
	def __init__(self):
		# general setup 
		super().__init__()
		self.screen = pg.display.get_surface()
		self.half_width = self.screen.get_size()[0] // 2
		self.half_height = self.screen.get_size()[1] // 2
		self.offset = pg.math.Vector2()

	# creating the floor
	def location_draw(self,location):

		self.ground_surf = pg.image.load('maps/' + location + '/' + location + '.png').convert()
		self.ground_rect = self.ground_surf.get_rect(topleft = (0,0))

	def custom_draw(self,player):

		# getting the offset 
		self.offset.x = player.rect.centerx - self.half_width
		self.offset.y = player.rect.centery - self.half_height

		ground_offset_pos = self.ground_rect.topleft - self.offset
		self.screen.blit(self.ground_surf,ground_offset_pos)

		# for sprite in self.sprites():
		for sprite in sorted(self.sprites(),key = lambda sprite: sprite.rect.centery):
			offset_pos = sprite.rect.topleft - self.offset
			self.screen.blit(sprite.image,offset_pos)

	def enemy_update(self,player):
		enemy_sprites = [sprite for sprite in self.sprites() if hasattr(sprite,'sprite_type') and sprite.sprite_type == 'enemy']
		for enemy in enemy_sprites:
			enemy.enemy_update(player)

class Text():
	def __init__(self,screen,pos,text,font,size,clr):
		self.font = pg.font.Font(font, size)
		msg = self.font.render(text, True, clr)
		msg_rect = msg.get_rect(center=(pos[0],pos[1]))
		screen.blit(msg,msg_rect)
class Button():
	def __init__(self,screen,pos,text):
		image_des = get_sprite(0,TILESIZE*2.5,TILESIZE*4,TILESIZE,ss_ui)
		self.pressed = False
		self.image = image_des
		self.rect = self.image.get_rect(center=(pos[0]+TILESIZE*2,pos[1]+TILESIZE*0.5))
		self.mask = pg.mask.from_surface(self.image)
		self.text = text
		self.button_state()
		self.draw(screen,pos)

	def draw(self,screen,pos):
		screen.blit(self.image,pos)
		Text(screen,self.rect.center,self.text,FONT,26,black)
	
	def button_state(self):
		mouse_pos = pg.mouse.get_pos()
		image_sel = get_sprite(0,TILESIZE*1.5,TILESIZE*4,TILESIZE,ss_ui)
		image_click = get_sprite(0,TILESIZE*3.5,TILESIZE*4,TILESIZE,ss_ui)
		image_des = get_sprite(0,TILESIZE*2.5,TILESIZE*4,TILESIZE,ss_ui)
		if self.rect.collidepoint(mouse_pos):
			self.image = image_sel
			if pg.mouse.get_pressed()[0]:
				self.pressed = True
			else:
				if self.pressed == True:
					print('click')
					self.image = image_click
					self.pressed = False
		else:
			self.image = image_des

class Tile(pg.sprite.Sprite):
	def __init__(self,pos,groups,sprite_type,surface = pg.Surface((TILESIZE,TILESIZE))):
		super().__init__(groups)
		self.sprite_type = sprite_type
		self.image = surface
		if sprite_type == 'object':
			self.rect = self.image.get_rect(topleft = (pos[0],pos[1] - TILESIZE))
			self.hitbox = self.rect.inflate(0,-20)
		elif sprite_type == 'world1':
			self.rect = self.image.get_rect(topleft = pos)
			self.hitbox = self.rect	
		else:
			self.rect = self.image.get_rect(topleft = pos)
			self.hitbox = self.rect.inflate(0,-10)
class Entity(pg.sprite.Sprite):
	def __init__(self,groups):
		super().__init__(groups)
		self.frame_index = 0
		self.animation_speed = 0.15
		self.direction = pg.math.Vector2()
	# moves the sprite
	def move(self,speed):
		if self.direction.magnitude() != 0:
			self.direction = self.direction.normalize()

		self.hitbox.x += self.direction.x * speed
		self.collision('horizontal')
		self.hitbox.y += self.direction.y * speed
		self.collision('vertical')
		self.rect.center = self.hitbox.center
		self.rect.y = self.hitbox.y - 90
	
	# detects collisions
	def collision(self,direction):
		if direction == 'horizontal':
			for sprite in self.obstacle_sprites:
				if sprite.hitbox.colliderect(self.hitbox):
					if self.direction.x > 0: # moving right
						self.hitbox.right = sprite.hitbox.left
					if self.direction.x < 0: # moving left
						self.hitbox.left = sprite.hitbox.right

		if direction == 'vertical':
			for sprite in self.obstacle_sprites:
				if sprite.hitbox.colliderect(self.hitbox):
					if self.direction.y > 0: # moving down
						self.hitbox.bottom = sprite.hitbox.top
					if self.direction.y < 0: # moving up
						self.hitbox.top = sprite.hitbox.bottom

