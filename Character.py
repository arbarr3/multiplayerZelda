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
		self.rect.height = self.rect.height * self.resScale
		self.rect.width = self.rect.width * self.resScale
		self.image = pygame.transform.scale(self.image, self.rect.size)

class Player(Character):
	def __init__(self, vel, filename, x, y, resScale=1, numRows=None, numCols=None, windowFPS=None, animationFPS=None, directionPacket=None, actionPacket=None):
		pygame.sprite.Sprite.__init__(self)
		self.vel = vel
		self.resScale = resScale
		self.direction = "DOWN"
		if actionPacket != None:
			self.animatedAction = True
			self.upAction = animateSprite(filename, numRows, numCols, resScale, windowFPS, animationFPS, actionPacket["UP"][0], actionPacket["UP"][1], x, y)
			self.downAction = animateSprite(filename, numRows, numCols, resScale, windowFPS, animationFPS, actionPacket["DOWN"][0], actionPacket["DOWN"][1], x, y)
			self.leftAction = animateSprite(filename, numRows, numCols, resScale, windowFPS, animationFPS, actionPacket["LEFT"][0], actionPacket["LEFT"][1], x, y)
			self.rightAction = animateSprite(filename, numRows, numCols, resScale, windowFPS, animationFPS, actionPacket["RIGHT"][0], actionPacket["RIGHT"][1], x, y)
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
				self.direction = "UP"
				self.image = self.upAnim.image
				self.mask = self.upAnim.mask
				self.upAnim.update(window, pressedKeys, keymap, spriteGroup)
			elif pressedKeys[keymap["moveDn"]]:
				self.direction = "DOWN"
				self.image = self.downAnim.image
				self.mask = self.downAnim.mask
				self.downAnim.update(window, pressedKeys, keymap, spriteGroup)
			elif pressedKeys[keymap["moveLf"]]:
				self.direction = "LEFT"
				self.image = self.leftAnim.image
				self.mask = self.leftAnim.mask
				self.leftAnim.update(window, pressedKeys, keymap, spriteGroup)
			elif pressedKeys[keymap["moveRt"]]:
				self.direction = "RIGHT"
				self.image = self.rightAnim.image
				self.mask = self.rightAnim.mask
				self.rightAnim.update(window, pressedKeys, keymap, spriteGroup)

		if pressedKeys[keymap["action"]]:
			if self.animatedAction:
				if self.direction == "UP":
					self.image = self.upAction.image
					self.upAction.update(window, pressedKeys, keymap, spriteGroup) # These may seem uneccesary, but could be used for long-hold action animations
				elif self.direction == "DOWN":
					self.image = self.downAction.image
					self.downAction.update(window, pressedKeys, keymap, spriteGroup)
				elif self.direction == "LEFT":
					self.image = self.leftAction.image
					self.leftAction.update(window, pressedKeys, keymap, spriteGroup)
				elif self.direction == "RIGHT":
					self.image = self.rightAction.image
					self.rightAction.update(window, pressedKeys, keymap, spriteGroup)
		elif pressedKeys[keymap["moveUp"]]:
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
		else:
			if self.direction == "UP" and self.animated:
				self.image = self.upAnim.image
			elif self.direction == "DOWN" and self.animated:
				self.image = self.downAnim.image
			elif self.direction == "LEFT" and self.animated:
				self.image = self.leftAnim.image
			elif self.direction == "RIGHT" and self.animated:
				self.image = self.rightAnim.image
		window.blit(self.image, (self.rect.x,self.rect.y))



class Mob(Character):
	def __init__(self, vel, filename, x, y, resScale=1, numRows=None, numCols=None, windowFPS=None, animationFPS=None, directionPacket=None):
		pygame.sprite.Sprite.__init__(self)
		self.vel = vel
		self.resScale = resScale
		self.direction = "DOWN"		
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