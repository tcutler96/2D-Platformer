from game_state import GameState


class OptionsController(GameState):
    def __init__(self, main):
        super().__init__(main, display=('fade', 0.25, (0, 0, 0), (0, 0)),
                         menu=(['Controller', 'big'], [{0: ['Player Jump', [main.controls_handler.controls_settings['player_jump'][1]], 0,
                                                            main.controls_handler.controls_settings_default['player_jump'][1], False],
                                                        1: ['Player Dash', [main.controls_handler.controls_settings['player_dash'][1]], 0,
                                                            main.controls_handler.controls_settings_default['player_dash'][1], True],
                                                        2: ['Player Attack', [main.controls_handler.controls_settings['player_attack'][1]], 0,
                                                            main.controls_handler.controls_settings_default['player_attack'][1], True]}, 0, True, True]))

    def main_loop(self):
        self.running = True
        while self.running:
            if self.menu.options_reset:
                self.menu.options_reset = False
                activities = []
                for button_index in self.menu.button_data:
                    button_data = self.menu.button_data[button_index]
                    if button_data[5] in ['scroll', 'input']:
                        activities.append(button_data[0])
                self.main.controls_handler.reset_settings(activities, False)
            if self.menu.option_changed:
                self.menu.option_changed = False
            if self.running:
                self.update()
                self.draw_game_state()
                self.main.update()
        self.main.exit_state()

    def update(self):
        self.update_game_state()

    def reset(self, enter):
        self.reset_game_state(enter)
