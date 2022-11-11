import pygame as pg
from settings import *
from support import *


# enemy data needs to be put in monster classes
monster_data = {
	'squid': {'health': 100,'exp':100,'damage':20,'attack_type': 'slash', 'attack_sound':'../audio/attack/slash.wav', 'speed': 3, 'resistance': 3, 'attack_radius': 80, 'notice_radius': 360,
			 'animations':{'idle':[],'move':[],'attack':[]}},

	'raccoon': {'health': 300,'exp':250,'damage':40,'attack_type': 'claw',  'attack_sound':'../audio/attack/claw.wav','speed': 2, 'resistance': 3, 'attack_radius': 120, 'notice_radius': 400},
	'spirit': {'health': 100,'exp':110,'damage':8,'attack_type': 'thunder', 'attack_sound':'../audio/attack/fireball.wav', 'speed': 4, 'resistance': 3, 'attack_radius': 60, 'notice_radius': 350},
	'bamboo': {'health': 70,'exp':120,'damage':6,'attack_type': 'leaf_attack', 'attack_sound':'../audio/attack/slash.wav', 'speed': 3, 'resistance': 3, 'attack_radius': 50, 'notice_radius': 300}}


class Enemy(Entity):
	def __init__(self,monster_name,monster_moves,pos,groups,obstacle_sprites):
		# general setup
		super().__init__(groups)
		self.sprite_type = 'enemy'

		# graphics setup
		self.import_graphics(monster_name,monster_moves)
		self.status = 'idle'
		self.image = self.animations[self.status][self.frame_index]

		# movement
		self.rect = self.image.get_rect(topleft = pos)
		self.hitbox = self.rect.inflate(0,-10)
		self.obstacle_sprites = obstacle_sprites

		# player interaction
		self.can_attack = True
		self.attack_time = None
		self.attack_cooldown = 400
	
	# import graphics
	def import_graphics(self,name,moves):
		sheet = pg.image.load('graphics/monsters/'+ name +'.png').convert_alpha()
		self.animations = moves

		j = 0
		for animation in self.animations.keys():
			self.animations[animation] = import_animations(sheet,TILESIZE,TILESIZE,3,j)
			j += 1
	
	# distance to player
	def get_player_distance_direction(self,player):
		enemy_vec = pg.math.Vector2(self.rect.center)
		player_vec = pg.math.Vector2(player.rect.center)
		distance = (player_vec - enemy_vec).magnitude()

		if distance > 0:
			direction = (player_vec - enemy_vec).normalize()
		else:
			direction = pg.math.Vector2()

		return (distance,direction)

	#get status
	def get_status(self, player):
		distance = self.get_player_distance_direction(player)[0]

		if distance <= self.attack_radius and self.can_attack:
			if self.status != 'attack':
				self.frame_index = 0
			self.status = 'attack'
		elif distance <= self.notice_radius:
			self.status = 'move'
		else:
			self.status = 'idle'

	# actions
	def actions(self,player):
		if self.status == 'attack':
			self.attack_time = pg.time.get_ticks()
		elif self.status == 'move':
			self.direction = self.get_player_distance_direction(player)[1]
		else:
			self.direction = pg.math.Vector2()
	#animates enemie
	def animate(self):
		animation = self.animations[self.status]
		
		self.frame_index += self.animation_speed
		if self.frame_index >= len(animation):
			if self.status == 'attack':
				self.can_attack = False
			self.frame_index = 0

		self.image = animation[int(self.frame_index)]
		self.rect = self.image.get_rect(center = self.hitbox.center)

	# cooldown
	def cooldown(self):
		if not self.can_attack:
			current_time = pg.time.get_ticks()
			if current_time - self.attack_time >= self.attack_cooldown:
				self.can_attack = True

	#update
	def update(self):
		self.move(self.speed)
		self.animate()
		self.cooldown()

	def enemy_update(self,player):
		self.get_status(player)
		self.actions(player)

class Blob(Enemy):
	def __init__(self,pos,groups,obstacle_sprites):
		monster_name = 'blob'
		monster_move = {'idle':[],'move':[],'attack': []}
		super().__init__(monster_name,monster_move,pos,groups,obstacle_sprites)
		self.health = 10
		self.exp = 10
		self.speed = 3
		self.attack_damage = 1
		self.resistance = 0
		self.attack_radius = TILESIZE * 2
		self.notice_radius = TILESIZE * 4
		self.attack_type = 'basic'

class Rat(Enemy):
	def __init__(self,pos,groups,obstacle_sprites):
		monster_name = 'rat'
		monster_move = {'idle':[],'move':[],'attack': []}
		super.__init__(monster_name,monster_move,pos,groups,obstacle_sprites)
		self.health = 10
		self.exp = 10
		self.speed = 3
		self.attack_damage = 1
		self.resistance = 0
		self.attack_radius = TILESIZE * 2
		self.notice_radius = TILESIZE * 4
		self.attack_type = 'basic'