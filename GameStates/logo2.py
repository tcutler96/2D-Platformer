from game_state import GameState


class Logo2(GameState):
    def __init__(self, main):
        super().__init__(main, display=('fade_black', 2, (0, 0, 0), (0, 0)), background=main.state_name)

    def main_loop(self):
        self.running = True
        logo_timer = self.main.timer_handler.add_timer(3, 1)
        while self.running:
            if self.main.events_handler.check_key('e', 'pressed') or self.main.timer_handler.check_timer(logo_timer):
                self.main.change_state(state_name='MainMenu')
            if self.main.events_handler.check_key('q', 'pressed'):
                self.main.exit_state_number = 1
            if self.running:
                self.update()
                self.draw_game_state()
                self.main.update()

    def update(self):
        self.update_game_state()

    def reset(self, enter):
        self.reset_game_state(enter)
