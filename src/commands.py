from abc import ABCMeta, abstractmethod

class ICommand(metaclass=ABCMeta):
	@abstractmethod
	def execute():
		pass


class PlaceTileCommand(ICommand):
	def __init__(self, map_square, tile):
		self.map_square = map_square
		self.tile = tile
		self.past_tile = 0

	def execute(self):
		self.past_tile = self.map_square.tile_index
		self.map_square.tile_index = self.tile

	def undo(self):
		self.map_square.tile_index = self.past_tile

	def __eq__(self, other):
		if not isinstance(other, PlaceTileCommand):
			return NotImplemented

		return self.map_square == other.map_square and self.tile == other.tile

