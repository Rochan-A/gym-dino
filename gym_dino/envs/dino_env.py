import os
import pygame
import random
from pygame import *

import numpy as np

from .sprites.sprite_path import sprite_path

import gym
from gym import error, spaces, utils
from gym.utils import seeding

pygame.init()

scr_size = (width,height) = (600,150)
FPS = 60
gravity = 0.6

black = (0,0,0)
white = (255,255,255)
background_col = (235,235,235)

screen = pygame.display.set_mode(scr_size)
clock = pygame.time.Clock()
pygame.display.set_caption("T-Rex Rush")

def load_image(
	name,
	sizex=-1,
	sizey=-1,
	colorkey=None,
	):

	#fullname = os.path.join('sprites', name)
	fullname = sprite_path(name)
	image = pygame.image.load(fullname)
	image = image.convert()
	if colorkey is not None:
		if colorkey is -1:
			colorkey = image.get_at((0, 0))
		image.set_colorkey(colorkey, RLEACCEL)

	if sizex != -1 or sizey != -1:
		image = pygame.transform.scale(image, (sizex, sizey))

	return (image, image.get_rect())

def load_sprite_sheet(
		sheetname,
		nx,
		ny,
		scalex = -1,
		scaley = -1,
		colorkey = None,
		):
	#fullname = os.path.join(sheetname)
	fullname = sprite_path(sheetname)
	sheet = pygame.image.load(fullname)
	sheet = sheet.convert()

	sheet_rect = sheet.get_rect()

	sprites = []

	sizex = sheet_rect.width/nx
	sizey = sheet_rect.height/ny

	for i in range(0,ny):
		for j in range(0,nx):
			rect = pygame.Rect((j*sizex,i*sizey,sizex,sizey))
			image = pygame.Surface(rect.size)
			image = image.convert()
			image.blit(sheet,(0,0),rect)

			if colorkey is not None:
				if colorkey is -1:
					colorkey = image.get_at((0,0))
				image.set_colorkey(colorkey,RLEACCEL)

			if scalex != -1 or scaley != -1:
				image = pygame.transform.scale(image,(scalex,scaley))

			sprites.append(image)

	sprite_rect = sprites[0].get_rect()

	return sprites,sprite_rect

def disp_gameOver_msg(retbutton_image,gameover_image):
	retbutton_rect = retbutton_image.get_rect()
	retbutton_rect.centerx = width / 2
	retbutton_rect.top = height*0.52

	gameover_rect = gameover_image.get_rect()
	gameover_rect.centerx = width / 2
	gameover_rect.centery = height*0.35

	screen.blit(retbutton_image, retbutton_rect)
	screen.blit(gameover_image, gameover_rect)

def extractDigits(number):
	if number > -1:
		digits = []
		i = 0
		while(number/10 != 0):
			digits.append(number%10)
			number = int(number/10)

		digits.append(number%10)
		for i in range(len(digits),5):
			digits.append(0)
		digits.reverse()
		return digits

class Dino():
	def __init__(self,sizex=-1,sizey=-1):
		self.images,self.rect = load_sprite_sheet('dino.png',5,1,sizex,sizey,-1)
		self.images1,self.rect1 = load_sprite_sheet('dino_ducking.png',2,1,59,sizey,-1)
		self.rect.bottom = int(0.98*height)
		self.rect.left = width/15
		self.image = self.images[0]
		self.index = 0
		self.counter = 0
		self.score = 0
		self.isJumping = False
		self.isDead = False
		self.isDucking = False
		self.isBlinking = False
		self.movement = [0,0]
		self.jumpSpeed = 11.5

		self.stand_pos_width = self.rect.width
		self.duck_pos_width = self.rect1.width

	def draw(self):
		screen.blit(self.image,self.rect)

	def checkbounds(self):
		if self.rect.bottom > int(0.98*height):
			self.rect.bottom = int(0.98*height)
			self.isJumping = False

	def update(self):
		if self.isJumping:
			self.movement[1] = self.movement[1] + gravity

		if self.isJumping:
			self.index = 0
		elif self.isBlinking:
			if self.index == 0:
				if self.counter % 400 == 399:
					self.index = (self.index + 1)%2
			else:
				if self.counter % 20 == 19:
					self.index = (self.index + 1)%2

		elif self.isDucking:
			if self.counter % 5 == 0:
				self.index = (self.index + 1)%2
		else:
			if self.counter % 5 == 0:
				self.index = (self.index + 1)%2 + 2

		if self.isDead:
			self.index = 4

		if not self.isDucking:
			self.image = self.images[self.index]
			self.rect.width = self.stand_pos_width
		else:
			self.image = self.images1[(self.index)%2]
			self.rect.width = self.duck_pos_width

		self.rect = self.rect.move(self.movement)
		self.checkbounds()

		if not self.isDead and self.counter % 7 == 6 and self.isBlinking == False:
			self.score += 1

		self.counter = (self.counter + 1)

class Cactus(pygame.sprite.Sprite):
	def __init__(self,speed=5,sizex=-1,sizey=-1):
		pygame.sprite.Sprite.__init__(self,self.containers)
		self.images,self.rect = load_sprite_sheet('cacti-small.png',3,1,sizex,sizey,-1)
		self.rect.bottom = int(0.98*height)
		self.rect.left = width + self.rect.width
		self.image = self.images[random.randrange(0,3)]
		self.movement = [-1*speed,0]

	def draw(self):
		screen.blit(self.image,self.rect)

	def update(self):
		self.rect = self.rect.move(self.movement)

		if self.rect.right < 0:
			self.kill()

class Ptera(pygame.sprite.Sprite):
	def __init__(self,speed=5,sizex=-1,sizey=-1):
		pygame.sprite.Sprite.__init__(self,self.containers)
		self.images,self.rect = load_sprite_sheet('ptera.png',2,1,sizex,sizey,-1)
		self.ptera_height = [height*0.82,height*0.75,height*0.60]
		self.rect.centery = self.ptera_height[random.randrange(0,3)]
		self.rect.left = width + self.rect.width
		self.image = self.images[0]
		self.movement = [-1*speed,0]
		self.index = 0
		self.counter = 0

	def draw(self):
		screen.blit(self.image,self.rect)

	def update(self):
		if self.counter % 10 == 0:
			self.index = (self.index+1)%2
		self.image = self.images[self.index]
		self.rect = self.rect.move(self.movement)
		self.counter = (self.counter + 1)
		if self.rect.right < 0:
			self.kill()


class Ground():
	def __init__(self,speed=-5):
		self.image,self.rect = load_image('ground.png',-1,-1,-1)
		self.image1,self.rect1 = load_image('ground.png',-1,-1,-1)
		self.rect.bottom = height
		self.rect1.bottom = height
		self.rect1.left = self.rect.right
		self.speed = speed

	def draw(self):
		screen.blit(self.image,self.rect)
		screen.blit(self.image1,self.rect1)

	def update(self):
		self.rect.left += self.speed
		self.rect1.left += self.speed

		if self.rect.right < 0:
			self.rect.left = self.rect1.right

		if self.rect1.right < 0:
			self.rect1.left = self.rect.right

class Cloud(pygame.sprite.Sprite):
	def __init__(self,x,y):
		pygame.sprite.Sprite.__init__(self,self.containers)
		self.image,self.rect = load_image('cloud.png',int(90*30/42),30,-1)
		self.speed = 1
		self.rect.left = x
		self.rect.top = y
		self.movement = [-1*self.speed,0]

	def draw(self):
		screen.blit(self.image,self.rect)

	def update(self):
		self.rect = self.rect.move(self.movement)
		if self.rect.right < 0:
			self.kill()

class Scoreboard():
	def __init__(self,x=-1,y=-1):
		self.score = 0
		self.tempimages,self.temprect = load_sprite_sheet('numbers.png',12,1,11,int(11*6/5),-1)
		self.image = pygame.Surface((55,int(11*6/5)))
		self.rect = self.image.get_rect()
		if x == -1:
			self.rect.left = width*0.89
		else:
			self.rect.left = x
		if y == -1:
			self.rect.top = height*0.1
		else:
			self.rect.top = y

	def draw(self):
		screen.blit(self.image,self.rect)

	def update(self,score):
		score_digits = extractDigits(score)
		self.image.fill(background_col)
		for s in score_digits:
			self.image.blit(self.tempimages[s],self.temprect)
			self.temprect.left += self.temprect.width
		self.temprect.left = 0

class DinoEnv(gym.Env):
	metadata = {'render.modes': ['human']}

	def __init__(self):
		self.gamespeed = 4
		self.gameOver = False
		self.playerDino = Dino(44,47)
		self.new_ground = Ground(-1*self.gamespeed)
		self.scb = Scoreboard()
		self.counter = 0
		self.done = False

		self.cacti = pygame.sprite.Group()
		self.pteras = pygame.sprite.Group()
		self.clouds = pygame.sprite.Group()
		self.last_obstacle = pygame.sprite.Group()

		Cactus.containers = self.cacti
		Ptera.containers = self.pteras
		Cloud.containers = self.clouds

		self.temp_images, self.temp_rect = load_sprite_sheet('numbers.png',12,1,11,int(11*6/5),-1)
		HI_image = pygame.Surface((22,int(11*6/5)))
		HI_rect = HI_image.get_rect()
		HI_image.fill(background_col)
		HI_rect.top = height*0.1
		HI_rect.left = width*0.73

	def step(self, action):
		if not self.gameOver:
			if pygame.display.get_surface() == None:
				print("Couldn't load display surface")
				self.gameOver = True
			else:
				if action == 1:
					if not (self.playerDino.isJumping and self.playerDino.isDead):
						self.playerDino.isDucking = True

				if action != 1:
					self.playerDino.isDucking = False
					if action == 2:
						if self.playerDino.rect.bottom == int(0.98*height):
							self.playerDino.isJumping = True
							self.playerDino.movement[1] = -1*self.playerDino.jumpSpeed

			for c in self.cacti:
				c.movement[0] = -1*self.gamespeed
				if pygame.sprite.collide_mask(self.playerDino,c):
					self.playerDino.isDead = True

			for p in self.pteras:
				p.movement[0] = -1*self.gamespeed
				if pygame.sprite.collide_mask(self.playerDino,p):
					self.playerDino.isDead = True

			if len(self.cacti) < 2:
				if len(self.cacti) == 0:
					self.last_obstacle.empty()
					self.last_obstacle.add(Cactus(self.gamespeed,40,40))
				else:
					for l in self.last_obstacle:
						if l.rect.right < width*0.7 and random.randrange(0,50) == 10:
							self.last_obstacle.empty()
							self.last_obstacle.add(Cactus(self.gamespeed, 40, 40))

			if len(self.pteras) == 0 and random.randrange(0,200) == 10 and self.counter > 500:
				for l in self.last_obstacle:
					if l.rect.right < width*0.8:
						self.last_obstacle.empty()
						self.last_obstacle.add(Ptera(self.gamespeed, 46, 40))

			if len(self.clouds) < 5 and random.randrange(0,300) == 10:
				Cloud(width,random.randrange(height/5,height/2))

			self.playerDino.update()
			self.cacti.update()
			self.pteras.update()
			self.clouds.update()
			self.new_ground.update()
			self.scb.update(self.playerDino.score)

			if pygame.display.get_surface() != None:
				screen.fill(background_col)
				self.new_ground.draw()
				self.clouds.draw(screen)
				self.scb.draw()
				self.cacti.draw(screen)
				self.pteras.draw(screen)
				self.playerDino.draw()

			clock.tick(FPS)

			self.obs = pygame.surfarray.array3d(pygame.display.get_surface())

			if self.playerDino.isDead:
				self.gameOver = True

			if self.counter%700 == 699:
				self.new_ground.speed -= 1
				self.gamespeed += 1

			self.counter = (self.counter + 1)

		if self.gameOver:
			self.done = True
		return self.obs, self.playerDino.score, self.done, None

	def reset(self):
		self.gamespeed = 4
		self.gameOver = False
		self.playerDino = Dino(44,47)
		self.new_ground = Ground(-1*self.gamespeed)
		self.scb = Scoreboard()
		self.counter = 0
		self.done = False

		self.cacti = pygame.sprite.Group()
		self.pteras = pygame.sprite.Group()
		self.clouds = pygame.sprite.Group()
		self.last_obstacle = pygame.sprite.Group()

		Cactus.containers = self.cacti
		Ptera.containers = self.pteras
		Cloud.containers = self.clouds

		self.temp_images, self.temp_rect = load_sprite_sheet('numbers.png',12,1,11,int(11*6/5),-1)

	def render(self, mode='human'):
		pygame.display.update()

	def close(self):
		pygame.quit()