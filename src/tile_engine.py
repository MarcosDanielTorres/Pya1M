import pygame
import csv
from data.paths import *
import pygame.freetype
from commands import PlaceTileCommand
pygame.init()

font = pygame.font.Font(MAIN_LEVEL_EDITOR_FONT, 12)

from camera import Camera

print(Camera.world_rectangle)


class TileEngine:
	_instance = None
	map_width = 100								# Amount of tiles in the x-axis.
	map_height = 70								# Amount of tiles in the y-axis.
	tile_width = 16								# Width of a tile.
	tile_height = 16							# Height of a tile.
	tile_size = (tile_width, tile_height)		# Width and height of a tile in tuple form
	map_squares = []							# List of MapSquare objects.
	edit_mode = True 							#probably grid

	dirt_img = pygame.image.load(DIRT_TILE)
	grass_img = pygame.image.load(GRASS_TILE)

	transparent_img = pygame.image.load(TRANSPARENT_TILE)

	tile_indexes = {1: dirt_img, 2: grass_img}

	def __new__(class_, *args, **kwargs):
		if not isinstance(class_._instance, class_):
			class_._instance = object.__new__(class_, *args, **kwargs)
		return class_._instance


	"""
	TODO a function that loads the tile_indexes dict
	"""

	@classmethod
	def collision_test(self, rect, tiles):
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

	@classmethod
	def draw(self, display):
		""" Draws the previously loaded tile map and creates a list of non-passable tiles
		TODO: should deal with tiles that are passable but when interacted with, a collission occurs.
		 i.e coins, enemies and such.
		"""

		# todo: clean up the break part and the double call to screen...()

		viewport = Camera.viewport
		rect = self.screen_to_rect()
		for x in range(rect.x, rect.x + rect.width + 1):
			if x == self.map_width: break
			for y in range(rect.y, rect.y + rect.height + 1):
				if y == self.map_height: break
				screen_position_rect = self.map_square_to_screen_position(x, y)
				map_squares[x][y].draw(x, y, display, screen_position_rect)

		"""
		for x in range(self.map_width):
			for y in range(self.map_height):
				screen_position_rect = self.map_square_to_screen_position(x, y)
				map_squares[x][y].draw(x, y, display, screen_position_rect)
		"""

	@classmethod
	def update(self):
		self._update_collissions()

	@classmethod
	def _update_collissions(self):
		"""	Returns a list of collissionables pygame.Rect's."""

		rect_list = []
		for x in range(self.map_width):
			for y in range(self.map_height):
				if not map_squares[x][y].passable:
					rect_list.append(pygame.Rect(x * self.tile_width, y * self.tile_height, self.tile_width, self.tile_height))

		return rect_list


	# this method shouldn't be here, it should be in the grid
	@classmethod
	def handle_events(self, pos, current_tile):
		"""
		:param pos: the mouse position.
		:param scroll: the scroll value.
		:param zoom: zoom value.
		:param current_tile: the index of the current_tile as stored in tile_indexes.
		"""
		if pygame.mouse.get_pressed()[0] == 1:
			x, y  = self.screen_position_to_map_square(pos)
			return PlaceTileCommand(map_squares[x][y], current_tile)
		elif pygame.mouse.get_pressed()[2] == 1:
			x, y  = self.screen_position_to_map_square(pos)
			return PlaceTileCommand(map_squares[x][y], 0)

	@classmethod
	def initialize(self):
		""" Prepares an empty map."""

		self.clear_map()

		for x in range(self.map_width):
			map_row = []
			for y in range(self.map_height):
				map_row.append(MapSquare(0))
			map_squares.append(map_row)

	@classmethod
	def load_map(self, path):
		self.clear_map()
		"""Load a map from a .csv file

		:param path: the relative path of the map.
		TODO: probably should include a level.
		"""

		with open(f'{path}', newline='') as csvfile:
			reader = csv.reader(csvfile, delimiter=',')
			for i in range(self.map_width):
				lista = []
				for row in reader:
					elem = row[i].split(';')
					lista.append(MapSquare(elem[0], elem[1], elem[2]))
				map_squares.append(lista)
				csvfile.seek(0)

	@classmethod
	def save_map(self, path):
		"""Save a map to a .csv file

		:param path: the relative save path of the map.
		TODO: probably should include a level.
		"""

		with open(f'{path}', 'w', newline='') as csvfile:
			writer = csv.writer(csvfile, delimiter=',')
			for i in range(map_height):
				writer.writerow([row[i] for row in map_squares])

	@classmethod
	def clear_map(cls):
		""" Clears the content of the map squares list """

		global map_squares
		map_squares = []


	@classmethod
	def map_square_to_screen_position(self, x, y):
		""" Returns the screen position of the map square.
		:params x: row index of this MapSquare in the map_squares list.
		:params y: column index of this MapSquare in the map_squares list.
		returns a tuple representing the x, y coordinates of the MapSquare in the screen.
		"""

		return (int((x * self.tile_width - Camera.scroll[0]) * Camera.zoom),
				int((y * self.tile_height - Camera.scroll[1]) * Camera.zoom))


	@classmethod
	def screen_position_to_map_square(self, pos):
		"""
		:param pos: the mouse position.
		returns a tuple representing the x, y index of the MapSquare in the map_squares list.
		"""
		x = int((pos[0] + Camera.scroll[0] * Camera.zoom) // (self.tile_width * Camera.zoom))
		y = int((pos[1] + Camera.scroll[1] * Camera.zoom) // (self.tile_height * Camera.zoom))
		return (x, y)

	@classmethod
	def screen_to_rect(cls):
		"""
		:param scroll: the scroll value.
		:param zoom: zoom value.
		returns a tuple representing the x, y index of the MapSquare in the map_squares list.
		"""
		x = int((Camera.scroll[0] * Camera.zoom) // (cls.tile_width * Camera.zoom))
		y = int((Camera.scroll[1] * Camera.zoom) // (cls.tile_height * Camera.zoom))
		width = int((Camera.viewport_width * Camera.zoom) // (cls.tile_width * Camera.zoom))
		height = int((Camera.viewport_height * Camera.zoom) // (cls.tile_height * Camera.zoom))
		return pygame.Rect(x, y, width, height)


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

cache_system = {1: {}, 2: {}}

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

	def draw(self, x, y, display, screen_position_rect):
		"""	Draws this MapSquare.

		:params x: row index of this MapSquare in the map_squares list.
		:params y: column index of this MapSquare in the map_squares list.
		:params display: pygame.Surface in which this MapSquare will be drawn.
		:params scroll: the scroll value.
		:params zoom: the zoom value.
		"""
		# {1: {zoom_level: dirt_img}, 2: {zoom_level: grass_img}}	

		if self.tile_index != 0:
			if cache_system[self.tile_index].get(Camera.zoom) == None:
				scaled_img = pygame.transform.scale(
					TileEngine.tile_indexes[self.tile_index], (int(Camera.zoom * TileEngine.tile_width), int(Camera.zoom * TileEngine.tile_height)))
				cache_system[self.tile_index][Camera.zoom] = scaled_img

			display.blit(cache_system[self.tile_index][Camera.zoom],
				 screen_position_rect)

		if TileEngine.edit_mode:
			if Camera.zoom > 3 and self.code != "":
					display.blit(
						TileEngine.multiLineSurface(self.code, font, pygame.Rect(x, y, TileEngine.tile_width * Camera.zoom, TileEngine.tile_width * Camera.zoom),
						(0,0,0), (255,255,255)),
						screen_position_rect)

			if not self.passable:
				display.blit(
					pygame.transform.scale(TileEngine.transparent_img, (int(Camera.zoom * TileEngine.tile_width), int(Camera.zoom * TileEngine.tile_height))),
					screen_position_rect)



