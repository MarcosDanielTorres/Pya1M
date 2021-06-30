import pygame
import sys
import csv
import pickle
from PIL import ImageFont
import math

sys.path.append('..')

from gui.gui import ToolBar, Group, ListView
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

MAP_WIDTH = tile_engine.map_width
MAP_HEIGHT = tile_engine.map_height 



current_tile = 1
zoom = 1
zoom_increment = .1
zoom_in = False
zoom_out = False
revert_zoom = False
mousewheelup = False
mousewheeldown = False
ctrl = False
zoom_used = False

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
	global level, scrolling_left, scrolling_right, scrolling_up, scrolling_down, zoom_in, zoom_out, revert_zoom
	global mousewheelup, mousewheeldown, ctrl

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		if event.type == pygame.MOUSEBUTTONDOWN:
			if event.button == 4:
				mousewheelup = True
			if event.button == 5:
				mousewheeldown = True


		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_LCTRL:
				ctrl = True
			if event.key == pygame.K_r:
				revert_zoom = True
			if event.key == pygame.K_w: 
				scrolling_up = True 
			if event.key == pygame.K_s:
				scrolling_down = True 
			if event.key == pygame.K_a: 
				scrolling_left = True
			if event.key == pygame.K_d:
				scrolling_right = True

		if event.type == pygame.KEYUP:
			if event.key == pygame.K_LCTRL:
				ctrl = False 
			if event.key == pygame.K_r:
				revert_zoom = False
			if event.key == pygame.K_a:
				scrolling_left = False
			if event.key == pygame.K_d:
				scrolling_right = False
			if event.key == pygame.K_w: 
				scrolling_up = False 
			if event.key == pygame.K_s:
				scrolling_down = False 





def draw_grid():
	# vertical lines
	for c in range(MAP_WIDTH + 1):
		pygame.draw.line(tile_map, LIGHTGREY, (int((c * TILE_SIZE - scroll[0]) * zoom), 0), (int((c * TILE_SIZE - scroll[0]) * zoom), int(TILE_MAP_HEIGHT * zoom)))
	# horizontal lines
	for c in range(MAP_HEIGHT + 1):
		pygame.draw.line(tile_map, LIGHTGREY, (0, int((c * TILE_SIZE - scroll[1]) * zoom)), (int(TILE_MAP_WIDTH * zoom), int((c * TILE_SIZE - scroll[1]) * zoom)))




def draw_text(screen, text, font, text_col, x,y, center=True):
	img = font.render(text, True, text_col)
	screen.blit(img, (x,y))
	return img.get_rect()


pygame.display.set_caption('Level Editor')
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
tile_map = pygame.Surface((TILE_MAP_WIDTH, TILE_MAP_HEIGHT)) 

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

tileset_listview = ListView(15, TILE_MAP_POS_Y, 320, 400)

group = Group("Tile Properties", 15, TILE_MAP_POS_Y + 420, 225, 100)
group.add_radiobutton("Toggle Passable", 20, 20, 8)
group.add_radiobutton("Code", 20, 45, 8)


scroll = [0,0]
true_scroll = [0, 0]
scrolling_right = False
scrolling_left = False



scrolling_up = False
scrolling_down = False


while True:
	screen.fill(SCREEN_COLOR)
	tile_map.fill((255,255,255))
	pos = pygame.mouse.get_pos()


	if ctrl:
		if mousewheelup:
			mousewheelup = False
			zoom += zoom_increment
			zoom_used = True
			zoom_in = True
			zoom_out = False 
		elif mousewheeldown:
			mousewheeldown = False
			zoom -= zoom_increment
			zoom_used = True
			zoom_out = True
			zoom_in = False
			if zoom < 1:
				zoom = 1
			if scroll[0] > 800:
				scroll[0] =  math.floor(MAP_WIDTH * TILE_SIZE - (TILES_PER_SCREEN_HORIZONTALLY / zoom) * TILE_SIZE)
			if scroll[1] > 480:
				scroll[1] = math.floor(MAP_HEIGHT * TILE_SIZE - (TILES_PER_SCREEN_VERTICALLY / zoom) * TILE_SIZE)
		else:
			zoom_used = False
	else:
		zoom_used = False

		
	if revert_zoom:
		zoom = 1
		if scroll[0] > 800:
			scroll[0] = 800 #should not be hardcoded
		if scroll[1] > 480:
			scroll[1] = 480 #should not be hardcoded


	scroll_right_limit = math.floor(MAP_WIDTH * TILE_SIZE - (TILES_PER_SCREEN_HORIZONTALLY / zoom) * TILE_SIZE)
	scroll_down_limit = math.floor(MAP_HEIGHT * TILE_SIZE - (TILES_PER_SCREEN_VERTICALLY / zoom) * TILE_SIZE)
	
	draw_grid()

	tileset_listview.draw(screen)

	tileset_listview.check()
	current_tile = tileset_listview.clicked_tile_index

	group.draw_group_label(screen)


	if scrolling_right:
		if scroll[0]  < scroll_right_limit:
			scroll[0] += 5
		else:
			scroll[0] = scroll_right_limit
	if scrolling_left:
		if scroll[0] > 0:
			scroll[0] -= 5
		else:
			scroll[0] = 0

	if scrolling_down:
		if scroll[1]  < scroll_down_limit:
			scroll[1] += 5
		else:
			scroll[1] = scroll_down_limit
	if scrolling_up:
		if scroll[1] > 0:
			scroll[1] -= 5
		else:
			scroll[1] = 0






	tile_engine.draw(tile_map, scroll, zoom)


	

	# should be in tile_engine.py
	if TILE_MAP_POS_X < pos[0] < TILE_MAP_POS_X + TILE_MAP_WIDTH and TILE_MAP_POS_Y < pos[1] < TILE_MAP_POS_Y + TILE_MAP_HEIGHT:
		x = int((pos[0] - TILE_MAP_POS_X + scroll[0] * zoom) // (TILE_SIZE * zoom))
		y = int((pos[1] - TILE_MAP_POS_Y + scroll[1] * zoom) // (TILE_SIZE * zoom))
		if pygame.mouse.get_pressed()[0] == 1:
			tile_engine.map_squares[x][y].tile_index = current_tile
		elif pygame.mouse.get_pressed()[2] == 1:
			tile_engine.map_squares[x][y].tile_index = 0

	"""
	print("MAP_WIDTH: ", MAP_WIDTH)	
	print("MAP_HEIGHT: ", MAP_HEIGHT)	
	print("TILES_PER_SCREEN_HORIZONTALLY: ", TILES_PER_SCREEN_HORIZONTALLY)
	print("TILES_PER_SCREEN_VERTICALLY: ", TILES_PER_SCREEN_VERTICALLY)
	print("SCROLL[0]: ", scroll[0])
	print("SCROLL[1]: ", scroll[1])
	print("ZOOM: ", zoom)
	print("POS: ", pos)
	print("scroll_right_limit: ", scroll_right_limit)
	"""



	tb.draw()
	process_events()


	screen.blit(tile_map, (TILE_MAP_POS_X, TILE_MAP_POS_Y))
	pygame.display.update()
	clock.tick(60)