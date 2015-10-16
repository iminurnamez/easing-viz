import pygame as pg
from .. import tools, prepare
from ..components.labels import Label, Blinker
from ..components.animation import Animation, Task


class SplashScreen(tools._State):
    def __init__(self):
        super(SplashScreen, self).__init__()
        sr = pg.display.get_surface().get_rect()
        self.font = prepare.FONTS["weblysleekuisb"]
        self.next = "TESTING"
        self.title = Label(self.font, 128, "Easing Visualizer", "dodgerblue",
                                {"center": (sr.centerx, -100)}, bg="black")
        self.title.alpha = 0
        self.instruction = Blinker(self.font, 48, "Click anywhere to start", "gray80",
                                             {"midbottom": (sr.centerx, sr.bottom - 20)}, 700)
        self.labels = [self.title]
        self.animations = pg.sprite.Group()
        self.make_animations(sr.centery)

    def make_animations(self, centery):
        drop = Animation(centery=centery, duration=3000, round_values=True,
                                 transition="out_bounce")
        drop.callback = self.add_instruction
        drop.start(self.title.rect)
        fade_in = Animation(alpha=240, duration=2000, round_values=True)
        fade_in.start(self.title)
        self.animations.add(drop, fade_in)

    def add_instruction(self):
        self.labels.append(self.instruction)

    def get_event(self, event):
        if event.type == pg.QUIT:
            self.done = True
            self.quit = True
        elif event.type in (pg.MOUSEBUTTONUP, pg.KEYUP):
            self.done = True

    def update(self, surface, keys, dt):
        self.animations.update(dt)
        self.title.image.set_alpha(self.title.alpha)
        self.instruction.update(dt)
        self.draw(surface)

    def draw(self, surface):
        surface.fill(pg.Color("black"))
        for label in self.labels:
            label.draw(surface)