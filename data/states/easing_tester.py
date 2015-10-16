import pygame as pg
from .. import tools, prepare
from ..components.labels import Label
from ..components.transitions import TRANSITIONS
from ..components.animation import Animation, Task


class Block(object):
    font = prepare.FONTS["weblysleekuisb"]
    def __init__(self, topleft, size, transition, colorname):
        self.rect = pg.Rect(topleft, size)
        self.transition = transition
        self.color = pg.Color(colorname)
        self.label = Label(self.font, 16, transition, colorname, {"midleft": (0, self.rect.centery)})
        self.active = True

    def draw(self, surface):
        self.label.draw(surface)
        if self.active:
            pg.draw.rect(surface, self.color, self.rect)


class EasingTest(tools._State):
    def __init__(self):
        super(EasingTest, self).__init__()
        self.font = prepare.FONTS["weblysleekuisb"]
        self.screen_rect = pg.display.get_surface().get_rect()
        sr = self.screen_rect
        self.set_goal(800)
        self.ani_duration = 2000
        self.ui_rect = pg.Rect((0,0), (sr.width, 30))
        self.all_off = Label(self.font, 24, "All Off", "white",
                                   {"bottomleft": (10, sr.bottom - 20)})
        self.timer_label = Label(self.font, 32, "{} ms".format(0), "white",
                                           {"midbottom": (sr.centerx, sr.bottom - 10)}) 
        self.labels = [self.all_off, self.timer_label]
        instructs = ("Left-click a color name to toggle", "Right-click to start animations")
        top = 0
        for instruct in instructs:
            self.labels.append(Label(self.font, 16, instruct, "antiquewhite", {"topleft": (825, top)}))
            top += 50
            
    def stop_timing(self):
        self.timing = False
        
    def set_goal(self, goal):
        self.goal = goal
        self.start_points = [(100, self.screen_rect.top),
                                   (100, self.screen_rect.bottom)]
        self.end_points = [(goal, self.screen_rect.top),
                                   (goal, self.screen_rect.bottom)]

    def make_blocks(self):
        left, top = 100, 0
        blocks = [Block((left, top + (22*i)), (20, 20), transition, color)
                      for i, (transition, color) in enumerate(TRANSITIONS)]
        for i, (transition, color) in enumerate(TRANSITIONS):
            block = Block((left, top), (20, 20), transition, color)
            blocks.append(block)
            top += 22
        return blocks
        
    def make_animations(self):
        self.animations = pg.sprite.Group()
        self.timer = 0
        self.timing = True
        for block in self.blocks:
            block.rect.left = 100
            goal = self.goal, block.rect.y
            ani = Animation(x=goal[0], y=goal[1], duration=self.ani_duration,
                                    transition=block.transition, round_values=True)
            ani.start(block.rect)
            self.animations.add(ani)
        stop_timing = Task(self.stop_timing, self.ani_duration)
        self.animations.add(stop_timing)        

    def startup(self, persistent):
        self.persist = persistent
        self.blocks = self.make_blocks()
        self.animations = pg.sprite.Group()
        self.timer = 0
        self.timing =False
        
    def get_event(self, event):
        if event.type == pg.QUIT:
            self.done = True
            self.quit = True
        elif event.type == pg.MOUSEBUTTONUP:
            if event.button == 3:
                self.make_animations()
            elif event.button == 1:
                if self.all_off.rect.collidepoint(event.pos):
                    for block in self.blocks:
                        block.active = False
                else:
                    for block in self.blocks:
                        if block.label.rect.collidepoint(event.pos):
                            block.active = not block.active

    def update(self, surface, keys, dt):
        if self.timing:
            self.timer += dt
        self.timer_label.set_text("{} ms".format(self.timer))
        self.animations.update(dt)
        self.draw(surface)

    def draw(self, surface):
        surface.fill(pg.Color("black"))
        pg.draw.line(surface, pg.Color("white"),
                           self.start_points[0], self.start_points[1], 2)
        pg.draw.line(surface, pg.Color("white"), 
                           self.end_points[0], self.end_points[1], 2)
        for block in self.blocks:
            block.draw(surface)
        for label in self.labels:
            label.draw(surface)
 