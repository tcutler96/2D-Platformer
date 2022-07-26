from game_state import GameState
from random import randint


class Game(GameState):
    def __init__(self, main):
        super().__init__(main, display=('fade_black', 1, (0, 0, 1), (0, 0)), background=main.state_name, tile_map=True,
                         game_objects=[('Winged_Potion', (-190, -110))], player=True)
        self.bubble_timer = self.main.timer_handler.add_timer(0.025, 0)

    def main_loop(self):
        self.running = True
        while self.running:
            if self.main.controls_handler.check_activity('game_menu'):
                self.main.audio_handler.play_sound('menu_button_click')
                self.main.change_state(state_name='GameMenu')
            if self.main.events_handler.check_key('q', 'pressed'):
                self.main.exit_state_number = 1
            if self.main.events_handler.check_key('e', 'held'):
                self.display.shake_screen(1, 10)
            if self.main.controls_handler.check_activity('game_save'):
                self.main.window.add_overlay_text('Game Saved...')
            if self.running:
                self.update()
                self.draw_game_state()
                self.main.update()
        self.main.exit_state()

    def update(self):
        self.update_game_state()
        self.scroll_screen()
        if self.main.timer_handler.check_timer(self.bubble_timer):
            self.main.state.particles_handler.add_particle(1, [-self.display.display_size[0] / 2 + self.display.scroll[0], 1.5 * self.display.display_size[0] + self.display.scroll[0], 1],
                                                           [-self.display.display_size[1] / 2 + self.display.scroll[1], 1.5 * self.display.display_size[1] + self.display.scroll[1], 1],
                                                           [-0.25, 0.25, 0], [-0.5, 0, 0], 0, -0.005, [1, 5, 0], 0, 0, False, (201, 255, 248), [1, 3, 0.01], (25, 25, 25), 'add', True)

    def scroll_screen(self):
        scroll = [0, 0]
        # horizontal
        scroll[0] += self.player.pos_x + self.display.scroll_offset[0] - self.display.true_scroll[0] - (self.display.display_size[0] - self.player.sprite_width) / 2 + \
            [self.display.display_size[0] // 4 if self.main.controls_handler.check_activity('player_look_right', 'held') and not
                self.main.controls_handler.check_activity('player_look_left', 'held') else 0][0] - \
            [self.display.display_size[0] // 4 if self.main.controls_handler.check_activity('player_look_left', 'held') and not
                self.main.controls_handler.check_activity('player_look_right', 'held') else 0][0]
        if self.player.flip_h:
            scroll[0] -= 1 * self.player.sprite_width
        else:
            scroll[0] += 1 * self.player.sprite_width
        if -0.5 <= self.player.velocity[0] <= 0.5:
            self.display.scroll_speed[0] = 40
        else:
            self.display.scroll_speed[0] = 20
        self.display.true_scroll[0] += min(max(scroll[0] * self.main.dt / self.display.scroll_speed[0], -self.display.max_scroll_speed[0]), self.display.max_scroll_speed[0])
        # vertical
        scroll[1] += self.player.pos_y + self.display.scroll_offset[1] - self.display.true_scroll[1] - \
            (self.display.display_size[1] - self.player.sprite_height) / 1.5 + \
            [self.display.display_size[1] // 3 if self.main.controls_handler.check_activity('player_look_down', 'held') and not
                self.main.controls_handler.check_activity('player_look_up', 'held') else 0][0] - \
            [self.display.display_size[1] // 5 if self.main.controls_handler.check_activity('player_look_up', 'held') and not
                self.main.controls_handler.check_activity('player_look_down', 'held') else 0][0]
        if self.player.velocity[1] <= 0:
            self.display.scroll_speed[1] = 30
        else:
            self.display.scroll_speed[1] = 15
        self.display.true_scroll[1] += min(max(scroll[1] * self.main.dt / self.display.scroll_speed[1], -self.display.max_scroll_speed[1]), self.display.max_scroll_speed[1])
        self.display.scroll = self.display.true_scroll.copy()
        self.display.scroll = [int(self.display.scroll[0]), int(self.display.scroll[1])]

    def reset(self, enter):
        if not enter:
            self.main.audio_handler.toggle_music_deafen()
        self.main.audio_handler.switch_music('game', self.display.transition_time)
        self.reset_game_state(enter)
