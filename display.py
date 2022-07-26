import pygame as pg
from random import randint


class Display:
    # display data format: (Transition Type, Transition Time, (Scroll Start X, Scroll Start Y, Reset Scroll), (Scroll Offset X, Scroll Offset Y))
    def __init__(self, main, transition_type, transition_time, scroll, scroll_offset):
        self.main = main
        self.display_size = self.main.display_size
        self.display = pg.Surface(self.display_size)
        self.transition_type = transition_type
        self.transition_time = transition_time
        self.scroll_offset = [scroll_offset[0] * self.main.tile_size, scroll_offset[1] * self.main.tile_size]
        self.scroll = [scroll[0] * self.main.tile_size + self.scroll_offset[0], scroll[1] * self.main.tile_size + self.scroll_offset[1]]
        if scroll[2]:
            self.scroll = [self.scroll[0] + int((self.main.tile_size - self.display_size[0]) / 2), self.scroll[1] + int((self.main.tile_size - self.display_size[1]) / 2)]
        self.true_scroll = self.scroll
        self.scroll_speed = [0, 0]
        self.max_scroll_speed = [5, 5]
        self.mouse = False
        self.screen_shake_time = 0
        self.screen_shake_amount = 0

    def set_camera(self, position, centre=False):
        if centre:
            position = position[0] - self.display_size[0] // 2, position[1] - self.display_size[1] // 2
        self.true_scroll = [position[0], position[1]]

    def shake_screen(self, shake_time, shake_amount):
        self.screen_shake_time = shake_time * self.main.fps_base
        self.screen_shake_amount = shake_amount

    def update(self):
        # self.main.state.particles_handler.add_particle(10, [self.scroll[0], self.scroll[0] + self.display_size[0], 0], self.scroll[1] + self.display_size[1] + 10, 0, [-2, 0, 0], 0, 0, 1, 0, 0.5, None, (0, 0, 0), 1, (255, 255, 255))
        if self.screen_shake_time > 0:
            self.screen_shake_time -= 1
            self.scroll[0] += randint(-self.screen_shake_amount, self.screen_shake_amount)
            self.scroll[1] += randint(-self.screen_shake_amount, self.screen_shake_amount)
            self.main.state.particles_handler.add_particle(2, [self.scroll[0] + self.display_size[0] // 2 - 10, self.scroll[0] + self.display_size[0] // 2 + 10, 1],
                                                           [self.scroll[1] + self.display_size[1] // 2 - 10, self.scroll[1] + self.display_size[1] // 2 + 10, 1],
                                                           [-7, 7, 0], [-7, 7, 0], 0, 0, [1, 5, 0], 0, 1, False, (20, 40, 60), 1, (0, 0, 0), None, True, 0.25)

    def draw(self, game_state):
        self.update()
        self.display.fill((0, 0, 0))
        if game_state.background:
            game_state.background.draw(self)
        if game_state.tile_map:
            game_state.tile_map.draw(self)
        if game_state.game_objects:
            for game_object in game_state.game_objects:
                game_object.draw(self)
        if game_state.player:
            game_state.player.draw(self)
        if game_state.background:
            game_state.background.draw(self, False)
        if game_state.particles_handler:
            game_state.particles_handler.draw(self)
        if game_state.menu:
            game_state.menu.draw(self)
