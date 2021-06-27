import pygame
import sys
import csv
import pickle
from PIL import ImageFont

sys.path.append('..')

from gui.gui import ToolBar
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


import ctypes

def GetTextDimensions(text, points, font):
    class SIZE(ctypes.Structure):
        _fields_ = [("cx", ctypes.c_long), ("cy", ctypes.c_long)]

    hdc = ctypes.windll.user32.GetDC(0)
    hfont = ctypes.windll.gdi32.CreateFontA(points, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, font)
    hfont_old = ctypes.windll.gdi32.SelectObject(hdc, hfont)

    size = SIZE(0, 0)
    ctypes.windll.gdi32.GetTextExtentPoint32A(hdc, text, len(text), ctypes.byref(size))

    ctypes.windll.gdi32.SelectObject(hdc, hfont_old)
    ctypes.windll.gdi32.DeleteObject(hfont)

    return (size.cx, size.cy)



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

def draw_group_label():
	x = 15
	y = TILE_MAP_POS_Y + 420
	width = 225 
	height = 100
	rect = pygame.Rect(x,y,width,height)
	#pygame.draw.rect(screen, BORDER_COLOR, (x, y, width, height), 1)
	#draw_text(screen, "Group Label", font, RED, x+15,y-9)
	draw_group_label_container(screen, "Group Label", rect)

	pygame.draw.circle(screen, WHITE, (x+25, y+20), 7)
	pygame.draw.circle(screen, BORDER_COLOR, (x+25, y+20), 8, 1)

	pygame.draw.circle(screen, WHITE, (x+25, y+45), 7)
	pygame.draw.circle(screen, BORDER_COLOR, (x+25, y+45), 8, 1)


def draw_group_label_container(screen, text, rect):
	text_rect = draw_text(screen, text, MAIN_FONT, BLACK, rect.x + 20, rect.y - 9)
	f = ImageFont.truetype(MAIN_LEVEL_EDITOR_FONT, 14)
	size = f.getsize(text)
	pygame.draw.line(screen, BORDER_COLOR, (rect.x, rect.y), (rect.x + 15, rect.y))
	pygame.draw.line(screen, BORDER_COLOR, (rect.x + 20 + size[0] + 5, rect.y), (rect.x + rect.width, rect.y))

	pygame.draw.line(screen, BORDER_COLOR, (rect.x + rect.width, rect.y), (rect.x + rect.width, rect.y + rect.height))
	pygame.draw.line(screen, BORDER_COLOR, (rect.x + rect.width, rect.y + rect.height), (rect.x, rect.y + rect.height))
	pygame.draw.line(screen, BORDER_COLOR, (rect.x, rect.y + rect.height), (rect.x, rect.y))




pygame.display.set_caption('Level Editor')
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
tile_map = pygame.Surface((TILE_MAP_WIDTH, TILE_MAP_HEIGHT)) #MAP HEIGHT SHOULD BE TILES PER SCREEN VERTICALLY

TILE_MAP_POS_X = 430
TILE_MAP_POS_Y = 50 



tb = ToolBar(screen)

scroll = [0,0]
scrolling_right = False
scrolling_left = False
scroll_right_limit = MAP_WIDTH * TILE_SIZE - TILES_PER_SCREEN_HORIZONTALLY * TILE_SIZE

while True:
	screen.fill(SCREEN_COLOR)
	tile_map.fill((255,255,255))


	draw_grid()

	draw_listview_container() # obj listview
	draw_group_label() # obj group label


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


