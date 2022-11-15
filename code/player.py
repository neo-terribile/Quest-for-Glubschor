import pygame as pg 
from settings import *
from support import *
from items import Sword

class Player(Entity):
	def __init__(self,pos,groups,obstacle_sprites,create_attack,destroy_attack,create_magic):
		super().__init__(groups)
		self.image = get_sprite(0,0,TILESIZE,TILESIZE*2,ss_player)
		self.rect = self.image.get_rect(topleft = pos)
		self.mask = pg.mask.from_surface(self.image)
		self.hitbox = self.rect.inflate(-22,-96)
			
		# graphics setup
		self.import_player_assets()
		self.status = 'south'

		# movement 
		self.attacking = False
		self.attack_cooldown = 400
		self.attack_time = None
		self.obstacle_sprites = obstacle_sprites

		# weapon
		self.create_attack = create_attack
		self.destroy_attack = destroy_attack
		self.weapon_index = 0
		self.weapon = Sword
		self.can_switch_weapon = True
		self.weapon_switch_time = None
		self.switch_duration_cooldown = 200

		# magic 
		self.create_magic = create_magic
		self.magic_index = 0
		self.magic = list(magic_data.keys())[self.magic_index]
		self.can_switch_magic = True
		self.magic_switch_time = None

		self.strength = 50
		self.intelligence = 50
		self.dexterity = 50

		self.max_health = self.strength * 1.5
		self.max_energy = self.intelligence * 1.1
		self.health = self.max_health * 0.8
		if self.health > self.max_health:
			self.health = self.max_health
		self.energy = self.max_energy * 0.2
		if self.energy > self.max_energy:
			self.energy = self.max_energy
		self.speed = self.dexterity / 10

		# level
		self.level = 1
		self.exp_next_level = 10
		self.exp = 0

		# loot
		self.gold = 0

	# import player assets
	def import_player_assets(self):
		sheet = pg.image.load(ss_player).convert_alpha()
		self.animations =	{'north': [],'south': [],'west': [],'east': [],
							'northeast': [],'northwest': [],'southeast': [], 'southwest': [],
							'north_attack':[],'south_attack':[],'west_attack':[],'east_attack':[],
							'northeast_attack':[],'northwest_attack':[],'southeast_attack':[],'southwest_attack':[],
							'north_idle':[],'south_idle':[],'west_idle':[],'east_idle':[],
							'northeast_idle':[],'northwest_idle':[],'southeast_idle':[],'southwest_idle':[]}
		j = 0
		for animation in self.animations.keys():
			self.animations[animation] = import_animations(sheet,TILESIZE,TILESIZE*2,3,j)
			j += 1

	# player input
	def input(self):
		if not self.attacking:
			keys = pg.key.get_pressed()

			# movement input
			if keys[pg.K_UP]:
				if keys[pg.K_RIGHT]:
					self.direction.x = 1
					self.direction.y = -1
					self.status = 'northeast'
				elif keys[pg.K_LEFT]:
					self.direction.x = -1
					self.direction.y = -1
					self.status = 'northwest'
				else:
					self.direction.x = 0
					self.direction.y = -1
					self.status = 'north'

			elif keys[pg.K_DOWN]:
				if keys[pg.K_RIGHT]:
					self.direction.x = 1
					self.direction.y = 1
					self.status = 'southeast'
				elif keys[pg.K_LEFT]:
					self.direction.x = -1
					self.direction.y = 1
					self.status = 'southwest'
				else:
					self.direction.x = 0
					self.direction.y = 1
					self.status = 'south'

			else:	self.direction.y = 0

			if keys[pg.K_RIGHT]:
				if keys[pg.K_UP]:
					self.direction.x = 1
					self.direction.y = -1
					self.status = 'northeast'
				elif keys[pg.K_DOWN]:
					self.direction.x = 1
					self.direction.y = 1
					self.status = 'southeast'
				else:
					self.direction.x = 1
					self.direction.y = 0
					self.status = 'east'

			elif keys[pg.K_LEFT]:
				if keys[pg.K_UP]:
					self.direction.x = -1
					self.direction.y = -1
					self.status = 'northwest'
				elif keys[pg.K_DOWN]:
					self.direction.x = -1
					self.direction.y = 1
					self.status = 'southwest'
				else:
					self.direction.x = -1
					self.direction.y = 0
					self.status = 'west'
			else:
				self.direction.x = 0

			# attack input 
			if keys[pg.K_SPACE]:
				self.attacking = True
				self.attack_time = pg.time.get_ticks()
				self.create_attack()

			# magic input 
			if keys[pg.K_LCTRL]:
				self.attacking = True
				self.attack_time = pg.time.get_ticks()
				style = list(magic_data.keys())[self.magic_index]
				strength = list(magic_data.values())[self.magic_index]['strength'] + self.energy
				cost = list(magic_data.values())[self.magic_index]['cost']
				self.create_magic(style,strength,cost)

			if keys[pg.K_q] and self.can_switch_weapon:
				self.can_switch_weapon = False
				self.weapon_switch_time = pg.time.get_ticks()
				
				if self.weapon_index < len(list(weapon_data.keys())) - 1:
					self.weapon_index += 1
				else:
					self.weapon_index = 0
					
				self.weapon = list(weapon_data.keys())[self.weapon_index]

			if keys[pg.K_e] and self.can_switch_magic:
				self.can_switch_magic = False
				self.magic_switch_time = pg.time.get_ticks()
				
				if self.magic_index < len(list(magic_data.keys())) - 1:
					self.magic_index += 1
				else:
					self.magic_index = 0

				self.magic = list(magic_data.keys())[self.magic_index]

	# get player status
	def get_status(self):
		if self.direction.x == 0 and self.direction.y == 0:
			if not 'idle' in self.status and not 'attack' in self.status:
				self.status = self.status + '_idle'

		if self.attacking:
			self.direction.x = 0
			self.direction.y = 0
			if not 'attack' in self.status:
				if 'idle' in self.status:
					self.status = self.status.replace('_idle','_attack')
				else:
					self.status = self.status + '_attack'
		else:
			if 'attack' in self.status:
				self.status = self.status.replace('_attack','')

	# level up
	def level_up(self):
		if self.exp >= self.exp_next_level:
			self.level += 1
			self.exp_next_level = self.exp_next_level * self.level

	# cooldowns
	def cooldowns(self):
		current_time = pg.time.get_ticks()

		if self.attacking:
			if current_time - self.attack_time >= self.attack_cooldown:
				self.attacking = False
				self.destroy_attack()

		if not self.can_switch_weapon:
			if current_time - self.weapon_switch_time >= self.switch_duration_cooldown:
				self.can_switch_weapon = True

		if not self.can_switch_magic:
			if current_time - self.magic_switch_time >= self.switch_duration_cooldown:
				self.can_switch_magic = True

	# animate player
	def animate(self):
		animation = self.animations[self.status]

		# loop over the frame index 
		self.frame_index += self.animation_speed
		if self.frame_index >= len(animation):
			self.frame_index = 0

		# set the image
		self.image = animation[int(self.frame_index)]
		self.rect = self.image.get_rect(center = self.hitbox.center)
		
	# update player
	def update(self):
		self.input()
		self.cooldowns()
		self.get_status()
		self.animate()
		self.move(self.speed)
		self.level_up()