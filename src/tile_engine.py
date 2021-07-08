import pygame
import csv
from data.paths import *
import pygame.freetype
pygame.init()

#font = pygame.freetype.SysFont('Times New Roman', 12)
font = pygame.font.Font(MAIN_LEVEL_EDITOR_FONT, 12)

map_width = 100								# Amount of tiles in the x-axis.
map_height = 70								# Amount of tiles in the y-axis.
tile_width = 16								# Width of a tile.
tile_height = 16							# Height of a tile.
tile_size = (tile_width, tile_height)		# Width and height of a tile in tuple form
map_squares = []							# List of MapSquare objects.
edit_mode = True

dirt_img = pygame.image.load(DIRT_TILE)
grass_img = pygame.image.load(GRASS_TILE)

transparent_img = pygame.image.load(TRANSPARENT_TILE)



tile_indexes = {1: dirt_img, 2: grass_img}


"""
TODO a function that loads the tile_indexes dict
"""


def collision_test(rect, tiles):
	""" WARNING: YET TO BE USED. MAY HAVE BEEN USED IN game.py NOT SURE 

	Create a list of tiles that collide with a given rect

	:param rect: rect to be checked collisions with.
	:param tiles: a list of tiles to check against the rect.
	"""

	hit_list = []
	for tile in tiles:
		if rect.colliderect(tile):
			hit_list.append(tile)
	return hit_list


def draw(display, scroll, zoom):
	""" Draws the previously loaded tile map and creates a list of non-passable tiles
	TODO: should deal with tiles that are passable but when interacted with, a collission occurs.
	 i.e coins, enemies and such.
	"""

	for x in range(map_width):
		for y in range(map_height):
			map_squares[x][y].draw(x, y, display, scroll, zoom)




def update_collissions():
	"""	Returns a list of collissionables pygame.Rect's."""

	rect_list = []
	for x in range(map_width):
		for y in range(map_height):
			if not map_squares[x][y].passable:
				rect_list.append(pygame.Rect(x * tile_width, y * tile_height, tile_width, tile_height))

	return rect_list


def handle_events(pos, scroll, zoom, current_tile):
	"""
	:param pos: the mouse position.
	:param scroll: the scroll value.
	:param zoom: zoom value.
	:param current_tile: the index of the current_tile as stored in tile_indexes.
	"""
	if pygame.mouse.get_pressed()[0] == 1:
		x, y  = screen_position_to_map_square(pos, scroll, zoom)
		map_squares[x][y].tile_index = current_tile
	elif pygame.mouse.get_pressed()[2] == 1:
		x, y  = screen_position_to_map_square(pos, scroll, zoom)
		map_squares[x][y].tile_index = 0



def map_square_to_screen_position(x, y, scroll, zoom):
	""" Returns the screen position of the map square.

	:params x: row index of this MapSquare in the map_squares list.
	:params y: column index of this MapSquare in the map_squares list.
	:param scroll: the scroll value.
	:param zoom: zoom value.

	returns a tuple representing the x, y coordinates of the MapSquare in the screen.
	"""

	return (int((x * tile_width - scroll[0]) * zoom),
			int((y * tile_height - scroll[1]) * zoom))


def screen_position_to_map_square(pos, scroll, zoom):
	"""
	:param pos: the mouse position.
	:param scroll: the scroll value.
	:param zoom: zoom value.

	returns a tuple representing the x, y index of the MapSquare in the map_squares list.
	"""
	x = int((pos[0] + scroll[0] * zoom) // (tile_width * zoom))
	y = int((pos[1] + scroll[1] * zoom) // (tile_height * zoom))
	return (x, y)



class MapSquare:
	""" A specific square in the map

	Every MapSquare contains the index of the img to be used in every layer, the code that identifies
	the MapSquare (useful for map transitions, traps, etc) and if its passable meaning that a player can
	go through it.	Note: a tile may be passable but when collided with, a response should occur.
	i.e: the player colliding with a coin.
	"""

	def __init__(self, tile, code='', passable=True):
		""" Creates a new MapSquare
		
		# TO BE IMPLEMENTED
		:param background: the tile index that is going to get rendered in the background layer of the map square.
		:param interactive: the tile index that is going to get rendered in the interactive layer of the map square.
		:param foreground: the tile index that is going to get rendered in the foreground layer of the map square.
		# TO BE IMPLEMENTED
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

	def draw(self, x, y, display, scroll, zoom):
		"""	Draws this MapSquare.

		:params x: row index of this MapSquare in the map_squares list.
		:params y: column index of this MapSquare in the map_squares list.
		:params display: pygame.Surface in which this MapSquare will be drawn.
		:params scroll: the scroll value.
		:params zoom: the zoom value.
		"""
		screen_position_rect = map_square_to_screen_position(x, y, scroll, zoom)

		if self.tile_index != 0:
			display.blit(pygame.transform.scale(
					tile_indexes[self.tile_index], (int(zoom * tile_width), int(zoom * tile_height))),
				 screen_position_rect)

		if edit_mode:
			if zoom > 3 and self.code != "":
					display.blit(
						multiLineSurface(self.code, font, pygame.Rect(x, y, tile_width * zoom, tile_width * zoom),
						(0,0,0), (255,255,255)),
						screen_position_rect)

			if not self.passable:
				display.blit(
					pygame.transform.scale(transparent_img, (int(zoom * tile_width), int(zoom * tile_height))),
					screen_position_rect)



def initialize():
	""" Prepares an empty map."""

	clear_map()

	for x in range(map_width):
		map_row = []
		for y in range(map_height):
			map_row.append(MapSquare(0))
		map_squares.append(map_row)


def load_map(path):
	clear_map()
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

	global map_squares
	map_squares = []




def multiLineSurface(text, font, rect, text_col, bg_col ,justification=1):
		"""Returns a surface containing the passed text string, reformatted
		to fit within the given rect, word-wrapping as necessary. The text
		will be anti-aliased.

		Parameters
		----------
		string - the text you wish to render. \n begins a new line.
		font - a Font object
		rect - a rect style giving the size of the surface requested.
		fontColour - a three-byte tuple of the rgb value of the
				 text color. ex (0, 0, 0) = BLACK
		BGColour - a three-byte tuple of the rgb value of the surface.
		justification - 0 (default) left-justified
					1 horizontally centered
					2 right-justified

		Returns
		-------
		Success - a surface object with the text rendered onto it.
		Failure - raises a TextRectException if the text won't fit onto the surface.
		"""

		finalLines = []
		requestedLines = text.splitlines()
		# Create a series of lines that will fit on the provided
		# rectangle.
		for requestedLine in requestedLines:
			if font.size(requestedLine)[0] > rect.width:
				words = requestedLine.split('-')
				# if any of our words are too long to fit, return.
				for word in words:
					if font.size(word)[0] >= rect.width:
						raise TextRectException("The word " + word + " is too long to fit in the rect passed.")
				# Start a new line
				accumulatedLine = ""
				for word in words:
					testLine = accumulatedLine + word + " "
					# Build the line while the words fit.
					if font.size(testLine)[0] < rect.width:
						accumulatedLine = testLine
					else:
						finalLines.append(accumulatedLine)
						accumulatedLine = word + " "
				finalLines.append(accumulatedLine)
			else:
				finalLines.append(requestedLine)

		# Let's try to write the text out on the surface.
		surface = pygame.Surface(rect.size, pygame.SRCALPHA, 32)
		surface.fill((255,255,255,140))
		accumulatedHeight = 0
		for line in finalLines:
			if accumulatedHeight + font.size(line)[1] >= rect.height:
				 raise TextRectException("Once word-wrapped, the text string was too tall to fit in the rect.")
			if line != "":
				tempSurface = font.render(line, 1, text_col)
			if justification == 0:
				surface.blit(tempSurface, (0, accumulatedHeight))
			elif justification == 1:
				surface.blit(tempSurface, ((rect.width - tempSurface.get_width()) / 2, accumulatedHeight))
			elif justification == 2:
				surface.blit(tempSurface, (rect.width - tempSurface.get_width(), accumulatedHeight))
			else:
				raise TextRectException("Invalid justification argument: " + str(justification))
			accumulatedHeight += font.size(line)[1]
		return surface

class TextRectException:
		def __init__(self, message=None):
				self.message = message

		def __str__(self):
			return self.message