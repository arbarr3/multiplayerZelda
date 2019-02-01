import pygame
from pygame.locals import *

import random

class animateSprite(pygame.sprite.Sprite):
	def __init__(self, filename, numRows, numCols, resScale=1, windowFPS=60, animationFPS=60, startCell=0, endCell=0, xpos=0, ypos=0):
		pygame.sprite.Sprite.__init__(self)
		self.resScale = resScale
		self.sheet = pygame.image.load(filename).convert_alpha()
		self.sheetRect = self.sheet.get_rect()
		self.cellHeight = self.sheetRect.height/numRows
		self.cellWidth = self.sheetRect.width/numCols
		self.rows = numRows
		self.cols = numCols
		self.counterMax = int(windowFPS / animationFPS)
		self.counterPos = self.counterMax
		self.startCell = startCell
		self.endCell = endCell
		self.currentCell = self.startCell
		self.surfaces, self.masks = self.makeSurfaces()
		self.mask = self.masks[self.currentCell]
		self.image = self.surfaces[self.currentCell]
		self.rect = self.image.get_rect()
		self.rect.x = xpos
		self.rect.y = ypos

	def makeSurfaces(self):
		numCels = self.rows * self.cols
		surfaceList = []
		maskList = []
		for i in range(numCels):
			surf = pygame.Surface((self.cellWidth, self.cellHeight), pygame.SRCALPHA, 32).convert_alpha()
			surf.blit(self.sheet, (0,0), ((i/self.rows)*self.cellHeight, int(i/self.cols)*self.cellWidth, self.cellWidth, self.cellHeight))
			surfRect = surf.get_rect()
			surfRect.height = surfRect.height * self.resScale
			surfRect.width = surfRect.width * self.resScale
			surf = pygame.transform.scale(surf, surfRect.size)
			mask = pygame.mask.from_surface(surf)
			surfaceList.append(surf)
			maskList.append(mask)
		return surfaceList, maskList

	def setAnimCells(self, start, end):
		self.startCell = start
		self.endCell = end

	def nextFrame(self):
		if self.currentCell == self.endCell:
			self.currentCell = self.startCell
		else:
			self.currentCell += 1
		self.image = self.surfaces[self.currentCell]
		self.mask = self.masks[self.currentCell]

	def update(self, window, pressedKeys, keymap, spriteGroup):
		if self.counterPos == 0:
			self.counterPos = self.counterMax
			self.nextFrame()
		else:
			self.counterPos -= 1
		window.blit(self.image, self.rect)