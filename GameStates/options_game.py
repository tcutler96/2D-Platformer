from game_state import GameState


class OptionsGame(GameState):
    def __init__(self, main):
        super().__init__(main, display=('fade', 0.25, (0, 0, 0), (0, 0)),  # rethink and reorder options
                         menu=(['Game', 'big'], [{0: ['Particles', ['None', 'Low', 'Medium', 'High'], 3, 3, False],
                                                  1: ['Subtitles', ['On', 'Off'], 0, 0, True],
                                                  2: ['Controller Dead Zone', ['0', '0.05', '0.1', '0.15', '0.2', '0.25', '0.3', '0.35', '0.4', '0.45', '0.5'], 5, 5, False],
                                                  3: ['Toggle Ability', ['True', 'False'], 1, 1, True],
                                                  4: ['Directional Dashing', ['True', 'False'], 1, 1, True],
                                                  5: ['Place Holder', ['True', 'False'], 0, 0, True],
                                                  6: ['Place Holder', ['True', 'False'], 0, 0, True]}, 0, True, True]))

    def main_loop(self):
        self.running = True
        while self.running:
            if self.menu.options_reset:
                self.menu.options_reset = False
            if self.menu.option_changed:
                self.menu.option_changed = False
                if self.menu.button_selected == 0:
                    pass
                if self.menu.button_selected == 1:
                    pass
                if self.menu.button_selected == 2:
                    pass
                if self.menu.button_selected == 3:
                    pass
                if self.menu.button_selected == 4:
                    pass
            if self.running:
                self.update()
                self.draw_game_state()
                self.main.update()
        self.main.exit_state()

    def update(self):
        self.update_game_state()

    def reset(self, enter):
        self.reset_game_state(enter)
