import pygame as pg
import time
from helper import Helper
from settings_handler import SettingHandler
from window import Window
from audio_handler import AudioHandler
from controls_handler import ControlsHandler
from events_handler import EventsHandler
from timer_handler import TimerHandler
from font import Font
from transition import Transition
from GameStates import *


# add after effect section to display class that can add blur, limited circle vision, widescreen mode (black rect along top and bottom) for cutscenes, bloom, colour spread/ bleed...
# add wall sliding and jumping off wall
# simulate pausing of time when player is hit, distort noise and add visual effect (pg.mixer.pause/ unpause)
# simulate glowing effect by utilising alpha channel or blit(special_flags=BLEND_RGB_ADD) when outlining image
# create sprite sheet
# add hud with ability to toggle
# change sound volume before playing sound such that setting volume to 0 plays no sound
# change window top left icon
# resizing display does not re centre window
# add variable sound volume depending on range from player
# multiple reset/ transition fade to black doesn't work with menu transition set to fade, need to set display of first fade to black to a black screen, music also goes loud for a frame
# add automatic check for special keys (ie shift, ctrl, alt) in events handler check activity, 'shift + w' should not trigger both 'shift + w' and 'w' activities...
# have multiple sound files for same sound effect and randomly choose which one to play each time...
# add custom particles (i.e. sparks, flame) that are saved within the particle handler and can be accessed easily with particle_handler.custom_particle.sparks etc.

# have background image format 'Order_Bg/ Fg (0/ 1)_[Optional]X Parallax_Y Parallax', (0, 0) parallax default...
# fix all list comprehensions


class Main:
    def __init__(self):
        pg.mixer.pre_init(44100, -16, 2, 512)
        pg.init()
        pg.mixer.init()
        pg.mixer.set_num_channels(64)
        self.clock = pg.time.Clock()
        self.fps = 60
        self.fps_base = self.fps
        self.last_time = time.time()
        self.dt = 0
        self.dt_s = 0
        self.dt_ms = 0
        self.chunk_size = 8
        self.tile_size = 40
        self.display_size = (640, 360)
        self.game_title = '2D Platformer'
        self.helper = Helper(self)
        self.settings_handler = SettingHandler(self)
        self.window = Window(self)
        self.audio_handler = AudioHandler(self)
        self.controls_handler = ControlsHandler(self)
        self.events_handler = EventsHandler(self)
        self.timer_handler = TimerHandler(self)
        self.font = Font(self)
        self.debug_mode = False
        self.exit_state_number = 0
        self.transitions = []
        self.transition_reset = True
        self.state_dict = self.load_game_states()
        self.state_name = 'StartUp'
        self.state = self.state_dict[self.state_name]
        self.state_order = [self.state_name]
        self.state.main_loop()

    def load_game_states(self):
        state_dict = {}
        for file in self.helper.get_files('GameStates', 'py'):
            if file not in ['__init__.py', 'game_state_template.py']:
                file_name = file[:-3]
                self.state_name = ''.join([name.capitalize() for name in file_name.split('_')])
                state_object = getattr(eval(file_name), self.state_name)(self)
                state_dict[self.state_name] = state_object
        return state_dict

    def change_state(self, state_name):
        self.state_name = state_name
        self.state = self.state_dict[self.state_name]
        self.state_order.append(self.state_name)
        self.events_handler.reset()
        self.state.reset(enter=True)
        self.transitions.append(Transition(self))
        self.transitions[-1].main_loop()
        self.transitions.pop()

    def exit_state(self):
        self.state_order.pop()
        self.state_name = self.state_order[-1]
        self.state = self.state_dict[self.state_name]
        self.events_handler.reset()
        self.state.reset(enter=False)

    def pre_update(self):
        # include events handlers and timer_handler update functions
        # or just include at the end of the normal update function?
        self.events_handler.update()
        self.timer_handler.update()

    def update(self):
        if self.exit_state_number:
            self.state.running = False
            if self.exit_state_number >= len(self.transitions):
                self.exit_state_number = len(self.transitions) - 1
            if self.exit_state_number > 1 and self.transition_reset:
                self.transition_reset = False
                for i in range(self.exit_state_number):
                    if i == 0:
                        self.transitions[-(i + 1)].reset(position='start')
                    elif i == self.exit_state_number - 1:
                        self.transitions[-(i + 1)].reset(position='end')
                    else:
                        self.transitions[-(i + 1)].reset(position='middle')
            self.exit_state_number -= 1
        else:
            if self.events_handler.check_key('mouse1', 'held'):
                # self.state.particles_handler.add_particle(1, self.events_handler.mouse_pos[0] + self.state.display.scroll[0], self.events_handler.mouse_pos[1] + self.state.display.scroll[1],
                #                                           [-0.25, 0.25, 0], [-0.25, 0.25, 0], 0, 0, 1, 0, [1, 5, 1], False, (242, 235, 107), [1, 3, 0.1], (200, 100, 0), 'add')
                self.state.particles_handler.add_particle(1, [0, self.display_size[0], 1], [0, self.display_size[1], 1],
                                                          [-0.25, 0.25, 0], [-0.25, 0.25, 0], 0, 0, 1, 0, [1, 5, 1], False, (242, 235, 107), [1, 3, 0.1], (200, 100, 0), 'add')
                # self.state.particles_handler.add_particle(1, self.events_handler.mouse_pos[0] + self.state.display.scroll[0], self.events_handler.mouse_pos[1] + self.state.display.scroll[1],
                #                                           [-2, 2, 0], [-2, 2, 0], 0, 0, [1, 3, 1], [0.025, 0.05, 0], None, False, (255, [0, 255], 0))
                # self.state.particles_handler.add_particle(1, self.events_handler.mouse_pos[0] + self.state.display.scroll[0] + 10, self.events_handler.mouse_pos[1] + self.state.display.scroll[1],
                #                                           0, 0, 0, 0, 5, 0, None, True, (0, [0, 255], 125), [1, 4, 0.1], (125, 0, [0, 255]))
            if self.controls_handler.check_activity('main_quit_game'):
                self.change_state(state_name='Quit')
            if self.controls_handler.check_activity('main_debug_mode'):
                self.debug_mode = not self.debug_mode
            if self.controls_handler.check_activity('main_mouse'):
                self.window.mouse = not self.window.mouse
            if self.controls_handler.check_activity('main_update_default_settings'):
                self.settings_handler.update_default_settings()
            if self.events_handler.check_key('1', 'pressed'):
                self.window.add_overlay_text('Game Saved...')
            if self.events_handler.check_key('2', 'pressed'):
                self.window.add_overlay_text('Controller Disconnected...')
            self.events_handler.update()
            self.timer_handler.update()
            self.controls_handler.reset()
            self.window.draw(self.state.display)
            self.clock.tick(self.fps)
            self.dt = max((time.time() - self.last_time) * self.fps_base, 1)
            self.dt_s = time.time() - self.last_time
            self.dt_ms = round((time.time() - self.last_time) * 1000)
            self.last_time = time.time()
            self.transition_reset = True

    def update_transition(self, display):
        self.window.draw(display)
        self.clock.tick(self.fps)
        self.dt = max((time.time() - self.last_time) * self.fps_base, 1)
        self.dt_s = time.time() - self.last_time
        self.dt_ms = round((time.time() - self.last_time) * 1000)
        self.last_time = time.time()

    def quit_game(self):
        self.settings_handler.save_settings()


if __name__ == '__main__':
    Main()
