import os
import pygame as pg
from . import tools
#from .components import players

SCREEN_SIZE = (1080, 740)
ORIGINAL_CAPTION = "EASING EXAMPLES"

pg.init()
os.environ['SDL_VIDEO_CENTERED'] = "TRUE"
pg.display.set_caption(ORIGINAL_CAPTION)
SCREEN = pg.display.set_mode(SCREEN_SIZE)
SCREEN_RECT = SCREEN.get_rect()


FONTS = tools.load_all_fonts(os.path.join("resources", "fonts"))

