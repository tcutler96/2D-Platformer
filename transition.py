import pygame as pg
from game_state import GameState


class Transition(GameState):
    def __init__(self, main):
        super().__init__(main, display=('instant', 0, (0, 0, 0), (0, 0), False, False))
        self.old_state = self.main.state_dict[self.main.state_order[-2]]
        self.new_state = self.main.state
        self.display_old = self.old_state.display.display
        self.display_new = self.new_state.display.display
        self.display_cur = self.display_old
        self.transition = self.new_state.display.transition_type
        self.time, self.scale, self.step_size, self.switch = self.get_data()
        self.counter = 0
        self.entering = True
        self.switched = False
        self.finished = False

    def main_loop(self):
        self.running = True
        self.main.events_handler.timer_count = False
        while self.running:
            self.main.events_handler.update()
            if self.running:
                self.update()
                self.main.update_transition(self.display)

    def update(self):
        if self.counter >= self.time / 2 and not self.switched and self.switch:
            self.switch_display(self.entering)
            self.switched = True
        if self.counter >= self.time:
            self.finished = True
            if self.entering:
                self.counter = 0
                self.entering = False
                if self.switch:
                    self.switched = False
                else:
                    self.switched = True
                self.finished = False
                self.main.events_handler.timer_count = True
                self.new_state.main_loop()
                self.main.events_handler.timer_count = False
            else:
                self.main.events_handler.timer_count = True
                self.running = False
        if self.running:
            self.display.display.blit(self.display_cur, (0, 0))
            self.step()
            self.apply_transition()
            self.counter += 1

    def reset(self, position):
        if position == 'start':
            self.transition = 'fade_black'
            self.counter, self.time, self.scale, self.step_size, self.switch, self.switched = 0, self.main.fps, 0, 510 / self.main.fps, True, False
            self.display_old = pg.Surface(self.main.display_size)
        elif position == 'end':
            self.transition = 'fade_black'
            self.counter, self.time, self.scale, self.step_size, self.switch, self.switched = 0, self.main.fps, 0, 510 / self.main.fps, True, False
            self.display_cur = pg.Surface(self.main.display_size)
        elif position == 'middle':
            self.transition = 'instant'
            self.time, self.switch, self.switched = 0, True, False
            self.display_cur = pg.Surface(self.main.display_size)

    def switch_display(self, new=True):
        if new:
            self.display_cur = self.display_new
        else:
            self.display_cur = self.display_old

    def step(self):
        if not self.switched:
            self.scale += self.step_size
        else:
            self.scale -= self.step_size

    def fade_black(self):
        self.display.display.set_alpha(255 - self.scale)

    def fade(self):
        self.display_new.set_alpha(self.scale)
        self.display.display.blit(self.display_new, (0, 0))

    def blur(self):
        self.display.display = pg.transform.smoothscale(self.display.display, (int(self.display.display_size[0] / (self.scale + 1)), int(self.display.display_size[1] / (self.scale + 1))))
        self.display.display = pg.transform.smoothscale(self.display.display, self.display.display_size)

    def v_stretch(self):
        for _ in range(int(self.scale)):
            self.display.display = pg.transform.smoothscale(self.display.display, (int(self.display.display_size[0] / 1), int(self.display.display_size[1] / 2)))
            self.display.display = pg.transform.smoothscale(self.display.display, self.display.display_size)

    def h_stretch(self):
        for _ in range(int(self.scale)):
            self.display.display = pg.transform.smoothscale(self.display.display, (int(self.display.display_size[0] / 2), int(self.display.display_size[1] / 1)))
            self.display.display = pg.transform.smoothscale(self.display.display, self.display.display_size)

    def circle(self):
        pass
        # shrinking white circle on black rect and setting colour key to white, can centre circle on player...

    def rectangle(self):
        pass
        # simply move black rect from from left to right and switch display when fully covered

    def tv(self):
        pass
        # mimic turning off of a television

    def get_data(self):
        time = self.new_state.display.transition_time * self.main.fps
        scale = 0
        step_size = 0
        switch = True
        if self.transition == 'instant':
            time = 0
        elif self.transition == 'fade':
            scale = 0
            steps = 255
            step_size = steps / time
            switch = False
        elif self.transition == 'fade_black':
            scale = 0
            steps = 510
            step_size = steps / time
        elif self.transition == 'blur':
            scale = 0
            steps = 120
            step_size = steps / time
        elif self.transition == 'v_stretch':
            scale = 0
            steps = 120
            step_size = steps / time
        elif self.transition == 'h_stretch':
            scale = 0
            steps = 120
            step_size = steps / time
        elif self.transition == 'circle':
            scale = 0
            steps = 1
            step_size = steps / time
        elif self.transition == 'rectangle':
            scale = 0
            steps = 1
            step_size = steps / time
        elif self.transition == 'tv':
            scale = 0
            steps = 1
            step_size = steps / time
        return time, scale, step_size, switch
            
    def apply_transition(self):
        if self.transition == 'instant':
            pass
        elif self.transition == 'fade':
            self.fade()
        elif self.transition == 'fade_black':
            self.fade_black()
        elif self.transition == 'blur':
            self.blur()
        elif self.transition == 'v_stretch':
            self.v_stretch()
        elif self.transition == 'h_stretch':
            self.h_stretch()
        elif self.transition == 'circle':
            self.circle()
        elif self.transition == 'rectangle':
            self.rectangle()
        elif self.transition == 'tv':
            self.tv()
