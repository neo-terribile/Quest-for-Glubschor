import pygame as pg

class Weapon(pg.sprite.Sprite):
	def __init__(self,player,groups,image):
		super().__init__(groups)
		direction = player.status.split('_')[0]

		# graphic
		#full_path = f'graphics/weapons/{player.weapon}/{direction}.png'
		self.image = image
		
		# placement
		if direction == 'east':
			self.rect = self.image.get_rect(midleft = player.rect.midright + pg.math.Vector2(0,16))
		elif direction == 'west': 
			self.rect = self.image.get_rect(midright = player.rect.midleft + pg.math.Vector2(0,16))
		elif direction == 'south':
			self.rect = self.image.get_rect(midtop = player.rect.midbottom + pg.math.Vector2(-10,0))
		else:
			self.rect = self.image.get_rect(midbottom = player.rect.midtop + pg.math.Vector2(-10,0))

class Sword(Weapon):
	def __init__(self,player,groups):
		direction = player.status.split('_')[0]
		full_path = f'graphics/weapons/sword/{direction}.png'
		image = pg.image.load(full_path).convert_alpha()
		super().__init__(player,groups,image)
		self.image = pg.image.load(full_path).convert_alpha()
		self.cooldown = 400
		self.damage = 30