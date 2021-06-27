import pygame
import sys
import csv
import pickle
from PIL import ImageFont

sys.path.append('..')

from gui.gui import ToolBar, Group
import tile_engine
from data.paths import *
# To run as a standalone program.

pygame.init()
clock = pygame.time.Clock()

MAIN_FONT = pygame.font.Font(MAIN_LEVEL_EDITOR_FONT, 14)

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

TILE_MAP_WIDTH = 800
TILE_MAP_HEIGHT = 640

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (144, 201, 120)
RED = (200, 25, 25)
TEAL = (0,128,128)
LIGHTGREY = (128,128,128)
CYAN = (146, 244, 255)
BLACK = (0,0,0)
BORDER_COLOR = (130, 135, 144)
SCREEN_COLOR = (240, 240, 240)

level = 0


TILE_SIZE = tile_engine.tile_width
TILES_PER_SCREEN_HORIZONTALLY = TILE_MAP_WIDTH // TILE_SIZE
TILES_PER_SCREEN_VERTICALLY = TILE_MAP_HEIGHT // TILE_SIZE

GAP_BETWEEN_TILES = 5
MAP_WIDTH = tile_engine.map_width
MAP_HEIGHT = tile_engine.map_height 



current_tile = 1

""" TODO Explicar esto, si no se va a cargar nada se inicialziada pero si se carga un mapa tiene que borarse el mapa
	MAP_WIDTH Y HEIGHT de esta clase c orresponden a los mismos en tile e ngine, debería usar solo lo que está en tile engine
tile_engine.initialize()
tile_engine.clear_map()
tile_engine.load_map("Hola23.csv")
tile_engine.save_map("xd.csv")
print(tile_engine.map_squares)
"""
tile_engine.load_map("xd.csv")
tile_engine.save_map("xd-saved.csv")

def process_events():
	global level, scrolling_left, scrolling_right
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_UP: 
				level += 1
			if event.key == pygame.K_DOWN and level > 0:
				level -= 1
			if event.key == pygame.K_LEFT: 
				scrolling_left = True
			if event.key == pygame.K_RIGHT:
				scrolling_right = True
		if event.type == pygame.KEYUP:
			if event.key == pygame.K_LEFT:
				scrolling_left = False
			if event.key == pygame.K_RIGHT:
				scrolling_right = False





def draw_grid():
	# vertical lines
	for c in range(MAP_WIDTH + 1):
		pygame.draw.line(tile_map, LIGHTGREY, (c * TILE_SIZE - scroll[0], 0), (c * TILE_SIZE - scroll[0], TILE_MAP_HEIGHT))
	# horizontal lines
	for c in range(MAP_HEIGHT + 1):
		pygame.draw.line(tile_map, LIGHTGREY, (0, c * TILE_SIZE), (TILE_MAP_WIDTH, c * TILE_SIZE))

def draw_listview_container():
	x = 15
	y = TILE_MAP_POS_Y
	width = 320 
	height = 400
	pygame.draw.rect(screen, WHITE, (x-1, y-1, width-1, height-1))
	pygame.draw.rect(screen, BORDER_COLOR, (x, y, width, height), 1)


def draw_text(screen, text, font, text_col, x,y, center=True):
	img = font.render(text, True, text_col)
	screen.blit(img, (x,y))
	return img.get_rect()


pygame.display.set_caption('Level Editor')
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
tile_map = pygame.Surface((TILE_MAP_WIDTH, TILE_MAP_HEIGHT)) #MAP HEIGHT SHOULD BE TILES PER SCREEN VERTICALLY

TILE_MAP_POS_X = 430
TILE_MAP_POS_Y = 50

def about_test():
	print("My name is Marcos Daniel and I'm a developer from Argentina doing this project just for fun!")

def clear_test():
	tile_engine.initialize()


tb = ToolBar(screen)

tb_new = ToolBar.get_button('New')
tb_new.set_action(lambda: print("New"))
tb_save = ToolBar.get_button('Save')
tb_save.set_action(lambda: print("Save"))
tb_load = ToolBar.get_button('Load')
tb_load.set_action(lambda: print("Load"))

tb_interactive = ToolBar.get_button('Interactive')
tb_interactive.set_action(lambda: print("Interactive "))
tb_foreground = ToolBar.get_button('Foreground')
tb_foreground.set_action(lambda: print("Foreground"))
tb_background = ToolBar.get_button('Background')
tb_background.set_action(lambda: print("Background"))

tb_clear = ToolBar.get_button('Clear')
tb_clear.set_action(clear_test)

tb_about = ToolBar.get_button('About')
tb_about.set_action(about_test)


group = Group("Tile Properties", 15, TILE_MAP_POS_Y + 420, 225, 100)
group.add_radiobutton("Toggle Passable", 20, 20, 8)
group.add_radiobutton("Code", 20, 45, 8)


scroll = [0,0]
scrolling_right = False
scrolling_left = False
scroll_right_limit = MAP_WIDTH * TILE_SIZE - TILES_PER_SCREEN_HORIZONTALLY * TILE_SIZE

while True:
	screen.fill(SCREEN_COLOR)
	tile_map.fill((255,255,255))


	draw_grid()

	draw_listview_container() # obj listview

	group.draw_group_label(screen)


	if scrolling_right:
		if scroll[0]  < scroll_right_limit:
			scroll[0] += 5
	if scrolling_left:
		if scroll[0] > 0:
			scroll[0] -= 5

	tile_engine.draw(tile_map, scroll)


	pos = pygame.mouse.get_pos()

	if TILE_MAP_POS_X < pos[0] < TILE_MAP_POS_X + TILE_MAP_WIDTH and TILE_MAP_POS_Y < pos[1] < TILE_MAP_POS_Y + TILE_MAP_HEIGHT:
		x = (pos[0] - 430 + scroll[0]) // TILE_SIZE
		y = (pos[1] - 50) // TILE_SIZE
		if pygame.mouse.get_pressed()[0] == 1:
			tile_engine.map_squares[x][y].tile_index = current_tile
		elif pygame.mouse.get_pressed()[2] == 1:
			tile_engine.map_squares[x][y].tile_index = 0


	
	tb.draw()
	process_events()


	screen.blit(tile_map, (TILE_MAP_POS_X, TILE_MAP_POS_Y))
	pygame.display.update()
	clock.tick(60)


