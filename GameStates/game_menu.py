from game_state import GameState


class GameMenu(GameState):
    def __init__(self, main):
        super().__init__(main, display=('fade', 0.25, (0, 0, 0), (0, 0)),
                         menu=(['Paused', 'big'], [{0: ['Continue', None, 0, 0, False],
                                                    1: ['Options', None, 0, 0, False],
                                                    2: ['Quit', None, 0, 0, False]}, 0, False, True]))

    def main_loop(self):
        self.running = True
        while self.running:
            if self.menu.button_triggered:
                self.menu.button_triggered = False
                if self.menu.button_selected == 0:
                    self.running = False
                if self.menu.button_selected == 1:
                    self.main.change_state(state_name='Options')
                if self.menu.button_selected == 2:
                    self.main.change_state(state_name='GameMenuQuit')
            if self.running:
                self.update()
                self.draw_game_state()
                self.main.update()
        self.main.exit_state()

    def update(self):
        self.update_game_state()

    def reset(self, enter):
        if enter:
            self.main.audio_handler.toggle_music_deafen()
        self.reset_game_state(enter)
