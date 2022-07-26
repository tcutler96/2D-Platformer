from game_state import GameState


class OptionsAudio(GameState):
    def __init__(self, main):
        super().__init__(main, display=('fade', 0.25, (0, 0, 0), (0, 0)),
                         menu=(['Audio', 'big'], [{0: ['Master', ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10'], int(main.audio_handler.audio_settings['master_volume'] * 10),
                                                       str(int(main.audio_handler.audio_settings_default['master_volume'] * 10)), False],
                                                   1: ['Music', ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10'], int(main.audio_handler.audio_settings['music_volume'] * 10),
                                                       str(int(main.audio_handler.audio_settings_default['music_volume'] * 10)), False],
                                                   2: ['Sound', ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10'], int(main.audio_handler.audio_settings['sound_volume'] * 10),
                                                       str(int(main.audio_handler.audio_settings_default['sound_volume'] * 10)), False]}, 0, True, True]))

    def main_loop(self):
        self.running = True
        while self.running:
            if self.menu.options_reset:
                self.menu.options_reset = False
                self.main.audio_handler.reset_settings()
            if self.menu.option_changed:
                self.menu.option_changed = False
                if self.menu.button_selected == 0:
                    self.main.audio_handler.change_volume('master', self.menu.button_data[self.menu.button_selected][2] / 10)
                if self.menu.button_selected == 1:
                    self.main.audio_handler.change_volume('music', self.menu.button_data[self.menu.button_selected][2] / 10)
                if self.menu.button_selected == 2:
                    self.main.audio_handler.change_volume('sound', self.menu.button_data[self.menu.button_selected][2] / 10)
            if self.running:
                self.update()
                self.draw_game_state()
                self.main.update()
        self.main.exit_state()

    def update(self):
        self.update_game_state()

    def reset(self, enter):
        self.reset_game_state(enter)
