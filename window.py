import pygame as pg
import os
import numpy as np


class Window:
    # display_scale to window_size: 1-(640, 360), 2-(1280, 720), 3-(1920, 1080), 4-(2560, 1440)
    def __init__(self, main):
        self.main = main
        pg.display.set_caption(self.main.game_title)
        self.video_settings = self.main.settings_handler.settings['Video']
        self.video_settings_default = self.main.settings_handler.settings_default['Video']
        self.monitor_size = (pg.display.Info().current_w, pg.display.Info().current_h)
        self.display_size = self.main.display_size
        self.display_scale_min = 1
        self.display_scale_max = min(self.monitor_size[0] // self.display_size[0], self.monitor_size[1] // self.display_size[1])
        self.display_scale = min(max(self.video_settings['window_size'][0] // self.display_size[0], self.display_scale_min), self.display_scale_max)
        self.window_size = (self.display_size[0] * self.display_scale, self.display_size[1] * self.display_scale)
        self.video_settings['window_size'] = self.window_size
        self.display_scale_default = min(max(self.video_settings_default['window_size'][0] // self.display_size[0], self.display_scale_min), self.display_scale_max)
        self.video_settings_default['window_size'] = (self.display_size[0] * self.display_scale_default, self.display_size[1] * self.display_scale_default)
        # os.environ['SDL_VIDEO_WINDOW_POS'] = '%d,%d' % (int(self.monitor_size[0] - self.video_settings['window_size'][0]) / 2, int(self.monitor_size[1] - self.video_settings['window_size'][1]) / 2)
        if self.video_settings['fullscreen']:
            self.window = pg.display.set_mode(self.window_size, pg.FULLSCREEN, 32)
        else:
            self.window = pg.display.set_mode(self.window_size, 0, 32)
        self.menu_colour_1 = (255, 255, 255)
        self.menu_colour_2 = (0, 0, 100)
        self.overlay_text = []
        pg.mouse.set_visible(False)
        self.cursor = self.main.helper.outline_image('Assets/Misc/cursor.png', outline_colour=self.menu_colour_2)
        self.mouse = False
        self.debug_colour_1 = (255, 127, 80)
        self.debug_colour_2 = (139, 0, 0)

    def resize_window(self, size):
        if size == 'Fullscreen' and not self.video_settings['fullscreen']:
            self.window_size = self.monitor_size
            self.video_settings['window_size'] = self.window_size
            self.video_settings['fullscreen'] = True
            self.display_scale = self.window_size[0] / self.display_size[0]
            self.window = pg.display.set_mode(self.window_size, pg.FULLSCREEN, 32)
        else:
            window_size = tuple(map(int, size.split(' x ')))
            if window_size != self.video_settings['window_size']:
                self.window_size = tuple(map(int, size.split(' x ')))
                self.video_settings['window_size'] = self.window_size
                self.video_settings['fullscreen'] = False
                self.display_scale = self.window_size[0] / self.display_size[0]
                self.window = pg.display.set_mode(self.window_size, 0, 32)

    def add_overlay_text(self, text, time=5):
        self.overlay_text.append([text, time * self.main.fps_base, True])

    def grey_scale(self, surface):
        return pg.surfarray.make_surface(pg.surfarray.pixels3d(surface).dot([0.298, 0.587, 0.114])[:, :, None].repeat(3, axis=2))

    def draw(self, display):
        self.window.fill((0, 0, 0))
        # function which applies display surface filter/ after effect (ie grey scale, bloom effect)
        # display.display = self.grey_scale(display.display)
        self.window.blit(pg.transform.scale(display.display, self.window_size), (0, 0))
        self.draw_overlay()
        if self.main.debug_mode:
            self.draw_debug_mode()
        if self.mouse or display.mouse:
            if self.main.events_handler.check_key(['mouse1', 'mouse3'], 'held'):
                self.window.blit(pg.transform.scale(self.cursor, (int(self.cursor.get_width() * self.display_scale * 0.95),
                                                                  int(self.cursor.get_height() * self.display_scale * 0.95))), self.main.events_handler.mouse_pos_window)
            else:
                self.window.blit(pg.transform.scale(self.cursor, (int(self.cursor.get_width() * self.display_scale),
                                                                  int(self.cursor.get_height() * self.display_scale))), self.main.events_handler.mouse_pos_window)
        pg.display.update()

    def draw_overlay(self):
        # or have text fade in and out...
        text_height = self.window_size[1] * 0.8
        for text in self.overlay_text:
            if text[2]:
                self.main.font.draw(self.window, text[0], (self.window_size[0] * 0.5, text_height), self.menu_colour_1, self.menu_colour_2, 3, 1, 'shadow', 2, 'centre', 'bottom')
            text_height += self.window_size[1] * 0.05
            text[1] -= 1
            if text[1] == 0:
                self.overlay_text.remove(text)
            elif text[1] % (self.main.fps_base // 4) == 0:
                text[2] = not text[2]

    def draw_debug_mode(self):
        pg.draw.rect(self.window, self.debug_colour_1, pg.Rect(self.window_size[0] // 2, self.window_size[1] // 2 - 7 * self.display_scale,
                                                               self.display_scale, 15 * self.display_scale))
        pg.draw.rect(self.window, self.debug_colour_1, pg.Rect(self.window_size[0] // 2 - 7 * self.display_scale, self.window_size[1] // 2, 15 *
                                                               self.display_scale, self.display_scale))
        self.main.font.draw(self.window, 'debug mode', (5 * self.display_scale, 5 * self.display_scale), self.debug_colour_1, self.debug_colour_2, self.display_scale, 1, 'shadow')
        self.main.font.draw(self.window, f'{self.main.state_name}', (self.window_size[0] // 2, 5 * self.display_scale), self.debug_colour_1, self.debug_colour_2,
                            self.display_scale, 1, 'shadow', h_align='centre')
        self.main.font.draw(self.window, 'ver: 0.1.2', (self.window_size[0] - 5 * self.display_scale, 5 * self.display_scale), self.debug_colour_1, self.debug_colour_2,
                            self.display_scale, 1, 'shadow', h_align='right')
        self.main.font.draw(self.window, f'fps: {int(self.main.clock.get_fps())}', (5 * self.display_scale, self.window_size[1] - 5 * self.display_scale),
                            self.debug_colour_1, self.debug_colour_2, self.display_scale, 1, 'shadow', v_align='bottom')
        self.main.font.draw(self.window, 'tcgame', (self.window_size[0] - 5 * self.display_scale, self.window_size[1] - 5 * self.display_scale),
                            self.debug_colour_1, self.debug_colour_2, self.display_scale, 1, 'shadow', h_align='right', v_align='bottom')
        if self.main.state.player:
            if self.main.state.player.god_mode:
                self.main.font.draw(self.window, ['god mode' + i * ' +' for i in [self.main.state.player.god_mode_faster]][0], (5 * self.display_scale, 20 * self.display_scale),
                                    self.debug_colour_1, self.debug_colour_2, self.display_scale, 1, 'shadow')
            else:
                self.main.font.draw(self.window, f'{self.main.state.player.state}', (5 * self.display_scale, 20 * self.display_scale), self.debug_colour_1, self.debug_colour_2,
                                    self.display_scale, 1, 'shadow')
        self.main.font.draw(self.window, f'particles: {len(self.main.state.particles_handler.particles)}', (5 * self.display_scale, 35 * self.display_scale),
                            self.debug_colour_1, self.debug_colour_2, self.display_scale, 1, 'shadow')

    def reset_settings(self):
        self.resize_window(f'{self.video_settings_default["window_size"][0]} x {self.video_settings_default["window_size"][1]}')
