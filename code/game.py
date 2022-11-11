import pygame as pg
from random import choice
from support import *
from player import *
from enemy import *
from ui import UI

class Game(States):
	def __init__(self):
		States.__init__(self)
		# get the display surface 
		self.screen = pg.display.get_surface()

		# sprite group setup
		self.visible_sprites = YSortCameraGroup()
		self.obstacle_sprites = pg.sprite.Group()
		self.player_sprite = pg.sprite.Group()
		self.enemie_sprites = pg.sprite.Group()
		self.trigger_sprites = pg.sprite.Group()

		# attack sprites
		self.current_attack = None
		self.attack_sprites = pg.sprite.Group()
		self.attackable_sprites = pg.sprite.Group()

	def create_map(self):
		self.ground_surf = pg.image.load('maps/' + self.location + '/' + self.location + '.png').convert()
		self.ground_rect = self.ground_surf.get_rect(topleft = (0,0))

		layouts = {
			'block': import_csv_layout('maps/' + self.location + '/' + self.location + '_blocks.csv'),
			'grass': import_csv_layout('maps/' + self.location + '/' + self.location + '_grass.csv'),
			'object': import_csv_layout('maps/' + self.location + '/' + self.location + '_objects.csv'),
			'entities': import_csv_layout('maps/' + self.location + '/' + self.location + '_entities.csv')}
		graphics = {
			'grass': import_folder('graphics/grass'),
			'objects': import_folder('graphics/objects')}

		for style,layout in layouts.items():
			for row_index,row in enumerate(layout):
				for col_index, col in enumerate(row):
					if col != '-1':
						x = col_index * TILESIZE
						y = row_index * TILESIZE
						if style == 'block':
							if col == '0': Tile((x,y),[self.obstacle_sprites],'invisible')
							else:
								if col == '1': Tile((x,y),[self.trigger_sprites],'world1')
								elif col == '2':
									pass
						if style == 'grass':
							random_grass_image = choice(graphics['grass'])
							Tile((x,y),[self.visible_sprites,self.obstacle_sprites, self.attackable_sprites],'grass',random_grass_image)
						if style == 'object':
							surf = graphics['objects'][int(col)]
							Tile((x,y),[self.visible_sprites,self.obstacle_sprites],'object',surf)
						if style == 'entities':
							if col == '0':
								if len(self.player_sprite) == 0:
									self.player = Player(
										(x,y),
										[self.visible_sprites,
										self.player_sprite],
										self.obstacle_sprites,
										self.create_attack,
										self.remove_attack,
										self.create_magic)
								else:
									self.player.hitbox.x = x
									self.player.hitbox.y = y	

							else:
								if col == '1': Blob((x,y),
								[self.visible_sprites],
								self.obstacle_sprites)
								elif col == '2': pass #monster_name = 'spirit'
								elif col == '3': pass #monster_name ='raccoon'
								else: pass
	
	def create_attack(self):	
		self.current_attack = self.player.weapon(self.player,[self.visible_sprites, self.attack_sprites])

	def remove_attack(self):
		if self.current_attack:
			self.current_attack.kill()
		self.current_attack = None

	def create_magic(self,style,strength,cost):
		print(style)
		print(strength)
		print(cost)

	def remove_magic(self):
		if self.current_magic:
			self.current_magic.kill()
		self.current_magic = None

	def player_attack_logic(self):
		if self.attack_sprites:
			for attack_sprite in self.attack_sprites:
				collision_sprites = pg.sprite.spritecollide(attack_sprite,self.attackable_sprites,False)
				if collision_sprites:
					for target_sprite in collision_sprites:
						if target_sprite.sprite_type == 'grass':
							target_sprite.kill()
						else:
							target_sprite.get_damage(self.player,attack_sprite.sprite_type)

	def change_map(self,location):
		self.location = location
		for sprite in self.obstacle_sprites:
			sprite.kill() 
		for sprite in self.trigger_sprites:
			sprite.kill()

		self.create_map()

	def player_interactions(self):
		if self.trigger_sprites:
			for player_sprite in self.player_sprite:
				collision_sprites = pg.sprite.spritecollide(player_sprite,self.trigger_sprites,False)
				for target_sprite in collision_sprites:
						if target_sprite.sprite_type == 'world1':
							self.mapchange = True
							self.change_map(target_sprite.sprite_type)

	def cleanup(self):
		print('cleaning up Game state stuff')

	def startup(self):
		print('starting Game state stuff')
		self.mapchange = True
		self.location = 'hometown'
		self.create_map()

		# user interface 
		self.ui = UI()

	def get_event(self, event):
		if event.type == pg.MOUSEBUTTONDOWN:
			self.next = 'menu'
			self.done = True

	def update(self, screen, dt):
		self.draw(screen)

	def draw(self, screen):
		if self.mapchange == True:
			self.visible_sprites.location_draw(self.location)
			self.mapchange = False
		self.visible_sprites.custom_draw(self.player)
		self.visible_sprites.update()
		self.visible_sprites.enemy_update(self.player)
		self.player_interactions()
		self.player_attack_logic()
		self.ui.draw(self.player)