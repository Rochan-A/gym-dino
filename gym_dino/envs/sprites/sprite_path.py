import os

def sprite_path(file):
	rom = os.path.join(os.path.dirname(os.path.abspath(__file__)), file)
	return rom