import pygame
import csv
from data.paths import *

map_width = 30		# Amount of tiles in the x-axis.
map_height = 13		# Amount of tiles in the y-axis.
tile_width = 16		# Width of the tile.
tile_height = 16	# Height of the tile.
map_squares = []	# List of MapSquare objects.

dirt_img = pygame.image.load(DIRT_TILE)
grass_img = pygame.image.load(GRASS_TILE)


tile_indexes = {1: dirt_img, 2: grass_img}


def collision_test(rect, tiles):
	""" Create a list of tiles that collide with a given rect

	:param rect: rect to be checked collisions with.
	:param tiles: a list of tiles to check against the rect.
	"""
	hit_list = []
	for tile in tiles:
		if rect.colliderect(tile):
			hit_list.append(tile)
	return hit_list


def draw(display, scroll):
	""" Draws the previously loaded tile map and creates a list of non-passable tiles
	TODO: should deal with tiles that are passable but when interacted with, a collission occurs. i.e coins, enemies and such.
	"""
	rect_list = []
	for x in range(map_width):
		for y in range(map_height):
			tile_index = map_squares[x][y].tile_index
			if tile_index != 0:
				display.blit(tile_indexes[tile_index], (x * 16 - scroll[0], y * 16 - scroll[1]))
				if not map_squares[x][y].passable:
					rect_list.append(pygame.Rect(x * 16, y * 16, 16, 16))
	return rect_list


def initialize():
	""" Prepares an empty map.
	TODO: Evaluate if its existence is justified.
	"""
	for x in range(map_width):
		map_row = []
		for y in range(map_height):
			map_row.append(MapSquare(0))
		map_squares.append(map_row)


def load_map(path):
	"""Load a map from a .csv file

	:param path: the relative path of the map.
	TODO: probably should include a level.
	"""
	with open(f'{path}', newline='') as csvfile:
		reader = csv.reader(csvfile, delimiter=',')
		for i in range(map_width):
			lista = []
			for row in reader:
				elem = row[i].split(';')
				lista.append(MapSquare(elem[0], elem[1], elem[2]))
			map_squares.append(lista)
			csvfile.seek(0)


def save_map(path):
	"""Save a map to a .csv file

	:param path: the relative save path of the map.
	TODO: probably should include a level.
	"""

	with open(f'{path}', 'w', newline='') as csvfile:
		writer = csv.writer(csvfile, delimiter=',')
		for i in range(map_height):
			writer.writerow([row[i] for row in map_squares])


def clear_map():
	""" Clears the content of the map squares list """
	map_squares = []


def map_square_screen_position(x, y):
	""" Returns the screen position of the map square.
	:param x: x coordinate.
	:param y: y coordinate.
	TODO: evaluate if its necessary
	"""

	return [x * tile_width, y * tile_height]
	# return [x * tile_width - camera.pos[0], y * tile_height - camera.pos[1]]


class MapSquare:
	""" A specific square in the map

	Every MapSquare contains the index of the img to be used in every layer, the code that identifies
	the MapSquare (useful for map transitions, traps, etc) and if its passable meaning that a player can
	go through it.	Note: a tile may be passable but when collided with, a response should occur.
	i.e: the player colliding with a coin.
	"""

	def __init__(self, tile, code='', passable=True):
		""" Creates a new MapSquare
		
		:param background: the tile index that is going to get rendered in the background of the map square.
		:param interactive: the tile index that is going to get rendered in the interactive of the map square.
		:param foreground: the tile index that is going to get rendered in the foreground of the map square.
		:param code: a code identifying the entire MapSquare, used to apply map transitions, traps, special effects, etc
		:param passable: if True a player can go throught it.
		"""
		#self.layers_index = [foreground, interactive, background]
		self.tile_index = int(tile)
		self.code = code
		self.passable = bool(int(passable))

	def __repr__(self):
		""" Returns a MapSquare in the form of: i1;i2;i3

		:i1: self.tile_index.
		:i2: self.coode
		:i3: self.passable
		"""
		return f'{self.tile_index};{self.code};{int(self.passable)}'

	def toggle_passable(self):
		""" Inverts the bool value of self.passable"""
		self.passable = not self.passable