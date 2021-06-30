from data.paths import *

import tile_engine
import pygame
import sys 
from gui.gui import ToolBar

holaaaaaaaaaaaaaaaa
rece que ahí anduvo

clock = pygame.time.Clock()  # set up the clock

from pygame.locals import *  # import pygame modules

pygame.init()  # initiate pygame

pygame.display.set_caption('Pygame Window')  # set the window name

WINDOW_SIZE = (600, 400)  # set up window size
screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32)  # initiate screen

display = pygame.Surface((300, 200))


moving_right = False
moving_left = False
moving_up = False
moving_down = False

sscroll = [0, 0]

player_rect = pygame.Rect(100, 90, 20, 20)


tile_engine.load_map(LEVEL_1)
tile_engine.save_map(LEVEL_1_SAVED)

def handle_events2():
    for event in pygame.event.get():  # event loop
        if event.type == QUIT:  # check for window quit
            pygame.quit()  # stop pygame
            sys.exit()  # stop script
        if event.type == KEYDOWN:
            if event.key == K_q:
                pygame.quit()
                sys.exit()
            if event.key == K_RIGHT:
            	moving_right = True


def handle_events():
	for event in pygame.event.get():  # event loop
		if event.type == QUIT:  # check for window quit
			pygame.quit()  # stop pygame
			sys.exit()  # stop script
		if event.type == KEYDOWN:
			if event.key == K_RIGHT:
				moving_right = True
			if event.key == K_LEFT:
				moving_left = True
			if event.key == K_UP:
				moving_up = True
			if event.key == K_DOWN:
				moving_down = True
		if event.type == KEYUP:
			if event.key == K_RIGHT:
				moving_right = False
			if event.key == K_LEFT:
				moving_left = False
			if event.key == K_UP:
				moving_up = False
			if event.key == K_DOWN:
				moving_down = False


def move(rect, movement, tiles):
	collision_types = {'top': False, 'bottom': False, 'right': False, 'left': False}
	rect.x += movement[0]
	hit_list = tile_engine.collision_test(rect, tiles)
	for tile in hit_list:
		if movement[0] > 0:
			rect.right = tile.left
			collision_types['right'] = True
		elif movement[0] < 0:
			rect.left = tile.right
			collision_types['left'] = True
	rect.y += movement[1]
	hit_list = tile_engine.collision_test(rect, tiles)
	for tile in hit_list:
		if movement[1] > 0:
			rect.bottom = tile.top
			collision_types['bottom'] = True
		elif movement[1] < 0:
			rect.top = tile.bottom
			collision_types['top'] = True
	return rect, collision_types


while True:
	display.fill((146, 244, 255))

	sscroll[0] += (player_rect.x - sscroll[0] - 150 + 20 ) / 20
	sscroll[1] += (player_rect.y - sscroll[1] - 100 + 20 ) / 20
	scroll = sscroll.copy()
	scroll[0] = int(scroll[0])
	scroll[1] = int(scroll[1])



					

	player_movement = [0, 0]
	if moving_right:
		player_movement[0]+=2
	if moving_left:
		player_movement[0]-=2
	if moving_up:
		player_movement[1]-=2
	if moving_down:
		player_movement[1]+=2

	rect_list = tile_engine.draw(display, scroll)

	player_rect, collisions = move(player_rect, player_movement, rect_list)


	pygame.draw.rect(display, (255, 0, 0), (20 - scroll[0], 50 - scroll[1], 20, 20))
	pygame.draw.rect(display, (0, 0, 255), (player_rect.x - scroll[0], player_rect.y - scroll[1], player_rect.width, player_rect.height))

	for event in pygame.event.get():  # event loop
		if event.type == QUIT:  # check for window quit
			pygame.quit()  # stop pygame
			sys.exit()  # stop script
		if event.type == KEYDOWN:
			if event.key == K_RIGHT:
				moving_right = True
			if event.key == K_LEFT:
				moving_left = True
			if event.key == K_UP:
				moving_up = True
			if event.key == K_DOWN:
				moving_down = True
		if event.type == KEYUP:
			if event.key == K_RIGHT:
				moving_right = False
			if event.key == K_LEFT:
				moving_left = False
			if event.key == K_UP:
				moving_up = False
			if event.key == K_DOWN:
				moving_down = False
	
	
	surf = pygame.transform.scale(display, WINDOW_SIZE)
	screen.blit(surf, (0, 0))
	pygame.display.update()  # update display
	clock.tick(60)  # maintain 60 fps