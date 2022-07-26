from game_state import GameState


class StartUp(GameState):
    def __init__(self, main):
        super().__init__(main, display=('instant', 0, (0, 0, 0), (0, 0)))

    def main_loop(self):
        self.running = True
        while self.running:
            self.main.change_state(state_name='Logo')
            self.main.change_state(state_name='Quit')

    def reset(self, enter):
        self.reset_game_state(enter)
