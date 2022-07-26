from game_state import GameState


class Extras(GameState):
    def __init__(self, main):
        super().__init__(main, display=('fade', 0.25, (0, 0, 0), (0, 0)),
                         menu=(['Extras', 'big'], [{0: ['Credits', None, 0, 0, False]}, 0, True, True]))

    def main_loop(self):
        self.running = True
        while self.running:
            # self.main.events_handler.update()
            if self.menu.button_triggered:
                self.menu.button_triggered = False
                if self.menu.button_selected == 0:
                    self.main.change_state(state_name='ExtrasCredits')
            if self.running:
                self.update()
                self.draw_game_state()
                self.main.update()
        self.main.exit_state()

    def update(self):
        self.update_game_state()

    def reset(self, enter):
        self.reset_game_state(enter)
