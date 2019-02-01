import pygame
from pygame.locals import *
from Character import *

WIDTH = 256
HEIGHT = 176

resScale = 4

keymap = {"action": pygame.K_SPACE,
		  "moveUp": pygame.K_UP,
		  "moveDn": pygame.K_DOWN,
		  "moveLf": pygame.K_LEFT,
		  "moveRt": pygame.K_RIGHT,
		  "quitGm": pygame.K_ESCAPE}


pygame.init()

WINDOW_DIMENSION = (WIDTH * resScale, HEIGHT * resScale)
window = pygame.display.set_mode((WINDOW_DIMENSION), HWSURFACE | DOUBLEBUF | RESIZABLE)
FPS = 30
clock = pygame.time.Clock()

all_sprites = pygame.sprite.Group()


# ===== Not where this will ultimately go.  Placed here for testing purposes ==========================================================
player = Player(10, "sprites/linkSmallShield.png", 20, 20, resScale, 1, 12, FPS, 7, {"UP":[2,3], "DOWN": [0,1], "LEFT": [6,7], "RIGHT": [4,5]})
all_sprites.add(player)

steve = Mob(6, "sprites/redRockShooter.png", 90, 90, resScale, 1, 8, FPS, 7, {"UP":[6,7], "DOWN":[2,3], "LEFT":[0,1], "RIGHT":[4,5]})
rick = Mob(6, "sprites/redRockShooter.png", 210, 210, resScale, 1, 8, FPS, 7, {"UP":[6,7], "DOWN":[2,3], "LEFT":[0,1], "RIGHT":[4,5]})
jim = Mob(6, "sprites/redRockShooter.png", 340, 340, resScale, 1, 8, FPS, 7, {"UP":[6,7], "DOWN":[2,3], "LEFT":[0,1], "RIGHT":[4,5]})

all_sprites.add(steve)
all_sprites.add(rick)
all_sprites.add(jim)

mob_sprites = pygame.sprite.Group()
mob_sprites.add(steve)
mob_sprites.add(rick)
mob_sprites.add(jim)
# =====================================================================================================================================

runMainLoop = True
while runMainLoop:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			runMainLoop = False

	pressedKeys = pygame.key.get_pressed()
	if pressedKeys[keymap["quitGm"]]:
		runMainLoop = False

	# Update
	all_sprites.update(window, pressedKeys, keymap, all_sprites)

	# Draw / render
	window.fill((0,0,0))
	all_sprites.draw(window)
	pygame.display.update()
	clock.tick(FPS)