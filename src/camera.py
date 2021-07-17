import pygame

class Camera:

	_instance = None
	_scroll = pygame.Vector2(0, 0)
	_viewport_size = pygame.Vector2(0, 0)
	_zoom = 1
	_world_rectangle = None 

	def __new__(class_, *args, **kwargs):
		if not isinstance(class_._instance, class_):
			class_._instance = object.__new__(class_, *args, **kwargs)
		return class_._instance

	@property
	def zoom(self):
		return self._zoom

	@zoom.setter
	def zoom(self, value):
		self._zoom = value


	@property
	def scroll(self):
		return self._scroll

	@scroll.setter
	def scroll(self, value):
		self._scroll = [min(max(self.world_rectangle.x, value[0]), self.world_rectangle.width - self.viewport_width // self.zoom),
		 min(max(self.world_rectangle.y, value[1]), self.world_rectangle.height - self.viewport_height // self.zoom)]

	@property
	def world_rectangle(self):
		return self._world_rectangle

	@world_rectangle.setter
	def world_rectangle(self, value):
		self._world_rectangle = value

	@property
	def viewport_width(self):
		return int(self._viewport_size[0])

	@viewport_width.setter
	def viewport_width(self, value):
		self._viewport_size.x = value

	@property
	def viewport_height(self):
		return int(self._viewport_size[1])

	@viewport_height.setter
	def viewport_height(self, value):
		self._viewport_size.y = value

	@property
	def viewport(self):
		return pygame.Rect(int(self.scroll[0]), int(self.scroll[1]), self.viewport_width, self.viewport_height)

	def move(self, offset):
		self.scroll += offset

Camera = Camera()
"""
Camera.world_rectangle = pygame.Rect(0, 0, 1600, 1120)
Camera.viewport_width = 800
Camera.viewport_height = 640
print(Camera.world_rectangle)
print(Camera.scroll)
Camera.move(pygame.Vector2(1000, 0))
print(Camera.scroll)
"""


"""
		public static Rectangle ViewPort {
			get {
				return new Rectangle(
					(int)Position.X, (int)Position.Y, ViewPortWidth, ViewPortHeight);
			}
		}
		#endregion
"""