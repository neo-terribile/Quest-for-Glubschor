import pygame as pg
import sys
from settings import *
from menu import *
from game import Game

class StateMachine:
    def __init__(self):
        #self.__dict__.update(settings)
        self.done = False
        self.screen = pg.display.set_mode(RESOLUTION)
        self.clock = pg.time.Clock()

    def setup_states(self, state_dict, start_state):
        self.state_dict = state_dict
        self.state_name = start_state
        self.state = self.state_dict[self.state_name]

    def flip_state(self):
        self.state.done = False
        previous,self.state_name = self.state_name, self.state.next
        self.state.cleanup()
        self.state = self.state_dict[self.state_name]
        self.state.startup()
        self.state.previous = previous

    def update(self, dt):
        if self.state.quit:
            self.done = True
        elif self.state.done:
            self.flip_state()
        self.state.update(self.screen, dt)

    def event_loop(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.done = True
            self.state.get_event(event)

    def main_game_loop(self):
        while not self.done:
            dt = self.clock.tick(FPS)/1000.0
            self.event_loop()
            self.update(dt)
            pg.display.update()

app = StateMachine()
state_dict = {
    'intro': Intro(),
    'menu': Menu(),
    'game': Game()}

class QfG:
    app.setup_states(state_dict, 'intro')
    app.main_game_loop()
    pg.quit()
    sys.exit()