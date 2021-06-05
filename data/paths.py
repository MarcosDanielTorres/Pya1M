import os
import sys

def path(directory: str, filename: str):
	if directory:
		return os.path.abspath(os.path.join(ROOT_DIR, "%s/%s" % (directory, filename)))
	return os.path.abspath(os.path.join(ROOT_DIR, "%s" % filename))


def img_path(filename: str): return path("images", filename)
def level_path(filename: str): return path("levels", filename)


ROOT_DIR = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))

# images
DIRT_TILE = img_path("dirt.png")
GRASS_TILE = img_path("grass.png")

# levels
LEVEL_1 = level_path("level_1.csv")
LEVEL_1_SAVED = level_path("level_1_saved.csv")


__all__ = [
	"DIRT_TILE",
	"GRASS_TILE",
	"LEVEL_1",
	"LEVEL_1_SAVED"
]