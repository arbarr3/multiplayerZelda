from animateSprite import *
from pygame.locals import *


class Character(pygame.sprite.Sprite):
	def __init__(self, vel, filename, x, y, resScale):
		pygame.sprite.Sprite.__init__(self)
		self.vel = vel
		self.resScale = resScale
		self.image = pygame.image.load(filename).convert_alpha()
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.rect.height = self.rect.height * resScale
		self.rect.width = self.rect.width * resScale
		self.image = pygame.transform.scale(self.image, self.rect.size)

class Player(Character):
	def __init__(self, vel, filename, x, y, resScale=1, numRows=None, numCols=None, windowFPS=None, animationFPS=None, directionPacket=None):
		pygame.sprite.Sprite.__init__(self)
		self.vel = vel
		self.resScale = resScale
		if numRows != None and numCols != None:
			self.animated = True
			self.downAnim = animateSprite(filename, numRows, numCols, resScale, windowFPS, animationFPS, directionPacket["DOWN"][0], directionPacket["DOWN"][1], x, y)
			self.upAnim = animateSprite(filename, numRows, numCols, resScale, windowFPS, animationFPS, directionPacket["UP"][0], directionPacket["UP"][1], x, y)
			self.leftAnim = animateSprite(filename, numRows, numCols, resScale, windowFPS, animationFPS, directionPacket["LEFT"][0], directionPacket["LEFT"][1], x, y)
			self.rightAnim = animateSprite(filename, numRows, numCols, resScale, windowFPS, animationFPS, directionPacket["RIGHT"][0], directionPacket["RIGHT"][1], x, y)
			self.image = self.downAnim.image
			self.rect = self.downAnim.rect
			self.mask = self.downAnim.mask
		else:
			self.image = pygame.image.load(filename).convert_alpha()
			self.rect = self.image.get_rect()
			self.rect.x = x
			self.rect.y = y
			self.rect.height = self.rect.height * resScale
			self.rect.width = self.rect.width * resScale
			self.image = pygame.transform.scale(self.image, self.rect.size)


	def update(self, window, pressedKeys, keymap, spriteGroup):
		if self.animated:
			if pressedKeys[keymap["moveUp"]]:
				self.image = self.upAnim.image
				self.mask = self.upAnim.mask
				self.upAnim.update(window, pressedKeys, keymap, spriteGroup)
			elif pressedKeys[keymap["moveDn"]]:
				self.image = self.downAnim.image
				self.mask = self.downAnim.mask
				self.downAnim.update(window, pressedKeys, keymap, spriteGroup)
			elif pressedKeys[keymap["moveLf"]]:
				self.image = self.leftAnim.image
				self.mask = self.leftAnim.mask
				self.leftAnim.update(window, pressedKeys, keymap, spriteGroup)
			elif pressedKeys[keymap["moveRt"]]:
				self.image = self.rightAnim.image
				self.mask = self.rightAnim.mask
				self.rightAnim.update(window, pressedKeys, keymap, spriteGroup)

		if pressedKeys[keymap["moveUp"]]:
			self.rect.y -= self.vel
			collideList = pygame.sprite.spritecollide(self, spriteGroup, False)
			#TODO: Add collision detection for different types of objects
			if len(collideList) > 1:
				self.rect.y = collideList[1].rect.y + collideList[1].rect.width
		elif pressedKeys[keymap["moveDn"]]:
			self.rect.y += self.vel
			collideList = pygame.sprite.spritecollide(self, spriteGroup, False)
			#TODO: Add collision detection for different types of objects
			if len(collideList) > 1:
				self.rect.y = collideList[1].rect.y - collideList[1].rect.width
		elif pressedKeys[keymap["moveLf"]]:
			self.rect.x -= self.vel
			collideList = pygame.sprite.spritecollide(self, spriteGroup, False)
			#TODO: Add collision detection for different types of objects
			if len(collideList) > 1:
				self.rect.x = collideList[1].rect.x + collideList[1].rect.height
		elif pressedKeys[keymap["moveRt"]]:
			self.rect.x += self.vel
			collideList = pygame.sprite.spritecollide(self, spriteGroup, False)
			#TODO: Add collision detection for different types of objects
			if len(collideList) > 1:
				self.rect.x = collideList[1].rect.x - collideList[1].rect.height
		window.blit(self.image, (self.rect.x,self.rect.y))



class Mob(Character):
	def __init__(self, vel, filename, x, y, resScale=1, numRows=None, numCols=None, windowFPS=None, animationFPS=None, directionPacket=None):
		pygame.sprite.Sprite.__init__(self)
		self.vel = vel
		self.resScale = resScale
		if numRows != None and numCols != None:
			self.animated = True
			self.downAnim = animateSprite(filename, numRows, numCols, resScale, windowFPS, animationFPS, directionPacket["DOWN"][0], directionPacket["DOWN"][1], x, y)
			self.upAnim = animateSprite(filename, numRows, numCols, resScale, windowFPS, animationFPS, directionPacket["UP"][0], directionPacket["UP"][1], x, y)
			self.leftAnim = animateSprite(filename, numRows, numCols, resScale, windowFPS, animationFPS, directionPacket["LEFT"][0], directionPacket["LEFT"][1], x, y)
			self.rightAnim = animateSprite(filename, numRows, numCols, resScale, windowFPS, animationFPS, directionPacket["RIGHT"][0], directionPacket["RIGHT"][1], x, y)
			self.image = self.downAnim.image
			self.rect = self.downAnim.rect
			self.mask = self.downAnim.mask
			self.direction = "DOWN"
		else:
			self.image = pygame.image.load(filename).convert_alpha()
			self.rect = self.image.get_rect()
			self.rect.x = x
			self.rect.y = y
			self.rect.height = self.rect.height * self.resScale
			self.rect.width = self.rect.width * self.resScale
			self.image = pygame.transform.scale(self.image, self.rect.size)

	def update(self, window, pressedKeys, keymap, spriteGroup):
		if self.animated:
			if self.direction == "UP":
				self.image = self.upAnim.image
				self.mask = self.upAnim.mask
				self.upAnim.update(window, pressedKeys, keymap, spriteGroup)
			elif self.direction == "DOWN":
				self.image = self.downAnim.image
				self.mask = self.downAnim.mask
				self.downAnim.update(window, pressedKeys, keymap, spriteGroup)
			elif self.direction == "LEFT":
				self.image = self.leftAnim.image
				self.mask = self.leftAnim.mask
				self.leftAnim.update(window, pressedKeys, keymap, spriteGroup)
			elif self.direction == "RIGHT":
				self.image = self.rightAnim.image
				self.mask = self.rightAnim.mask
				self.rightAnim.update(window, pressedKeys, keymap, spriteGroup)

		action = random.randint(1,30)
		if action == 1:
			self.direction = "UP"
		elif action == 2:
			self.direction = "DOWN"
		elif action == 3:
			self.direction = "LEFT"
		elif action == 4:
			self.direction = "RIGHT"
		else:
			if self.direction == "UP":
				self.rect.y -= self.vel
				collideList = pygame.sprite.spritecollide(self, spriteGroup, False)
				#TODO: Add collision detection for different types of objects
				if len(collideList) > 1:
					pos = 0
					while collideList[pos].rect == self.rect:
						pos += 1
					self.rect.y = collideList[pos].rect.y + collideList[pos].rect.width
			elif self.direction == "DOWN":
				self.rect.y += self.vel
				collideList = pygame.sprite.spritecollide(self, spriteGroup, False)
				#TODO: Add collision detection for different types of objects
				if len(collideList) > 1:
					pos = 0
					while collideList[pos].rect == self.rect:
						pos += 1
					self.rect.y = collideList[pos].rect.y - collideList[pos].rect.width
			elif self.direction == "LEFT":
				self.rect.x -= self.vel
				collideList = pygame.sprite.spritecollide(self, spriteGroup, False)
				#TODO: Add collision detection for different types of objects
				if len(collideList) > 1:
					pos = 0
					while collideList[pos].rect == self.rect:
						pos += 1
					self.rect.x = collideList[pos].rect.x + collideList[pos].rect.height
			elif self.direction == "RIGHT":
				self.rect.x += self.vel
				collideList = pygame.sprite.spritecollide(self, spriteGroup, False)
				#TODO: Add collision detection for different types of objects
				if len(collideList) > 1:
					pos = 0
					while collideList[pos].rect == self.rect:
						pos += 1
					self.rect.x = collideList[pos].rect.x - collideList[pos].rect.height
		window.blit(self.image, (self.rect.x,self.rect.y))