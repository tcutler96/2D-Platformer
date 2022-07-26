from game_state import GameState


class OptionsVideo(GameState):
    def __init__(self, main):
        super().__init__(main, display=('fade', 0.25, (0, 0, 0), (0, 0)),
                         menu=(['Video', 'big'], [{0: ['Display Size', [f'{main.window.display_size[0] * scale} x {main.window.display_size[1] * scale}'
                                                                        for scale in range(1, main.window.display_scale_max + 1)] + ['Fullscreen'],
                                                       main.window.display_scale - [1 if not main.window.video_settings['fullscreen'] else 0][0],
                                                       f'{main.window.video_settings_default["window_size"][0]} x {main.window.video_settings_default["window_size"][1]}', False]}, 0, True, True]))

    def main_loop(self):
        self.running = True
        while self.running:
            if self.menu.options_reset:
                self.menu.options_reset = False
                self.main.window.reset_settings()
            if self.menu.option_changed:
                self.menu.option_changed = False
                if self.menu.button_selected == 0:
                    self.main.window.resize_window(self.menu.button_data[self.menu.button_selected][1][self.menu.button_data[self.menu.button_selected][2]])
            if self.running:
                self.update()
                self.draw_game_state()
                self.main.update()
        self.main.exit_state()

    def update(self):
        self.update_game_state()

    def reset(self, enter):
        self.reset_game_state(enter)
