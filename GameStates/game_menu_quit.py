from game_state import GameState


class GameMenuQuit(GameState):
    def __init__(self, main):
        super().__init__(main, display=('fade', 0.25, (0, 0, 0), (0, 0)),
                         menu=(['Quit to', 'small'], [{0: ['Main Menu', None, 0, 0, False],
                                                       1: ['Desktop', None, 0, 0, False],
                                                       2: ['Cancel', None, 0, 0, False]}, 2, False, True]))

    def main_loop(self):
        self.running = True
        while self.running:
            if self.menu.button_triggered:
                self.menu.button_triggered = False
                if self.menu.button_selected == 0:
                    self.main.exit_state_number = 3
                if self.menu.button_selected == 1:
                    self.main.change_state(state_name='Quit')
                if self.menu.button_selected == 2:
                    self.main.exit_state_number = 1
            if self.running:
                self.update()
                self.draw_game_state()
                self.main.update()
        self.main.exit_state()

    def update(self):
        self.update_game_state()

    def reset(self, enter):
        self.reset_game_state(enter)
