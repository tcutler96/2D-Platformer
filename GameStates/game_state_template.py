from game_state import GameState


class GameStateTemplate(GameState):
    def __init__(self, main):
        super().__init__(main, display=('instant', 0, (0, 0, 0), (0, 0)), background=[], tile_map=[], game_objects=[], player=[], menu=[])

    def main_loop(self):
        self.running = True
        while self.running:
            if self.main.controls.check_activity(''):
                pass
            if self.menu.button_triggered:
                self.menu.button_triggered = False
                if self.menu.button_selected == 0:
                    pass
                if self.menu.button_selected == 1:
                    pass
            if self.menu.option_changed:
                self.menu.option_changed = False
                if self.menu.options_reset:
                    self.menu.options_reset = False
                else:
                    if self.menu.button_selected == 0:
                        pass
                    if self.menu.button_selected == 1:
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
