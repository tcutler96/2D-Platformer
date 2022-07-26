from game_state import GameState


class Logo(GameState):
    def __init__(self, main):
        super().__init__(main, display=('fade', 2, (0, 0, 0), (0, 0)), background=main.state_name)

    def main_loop(self):
        self.running = True
        timer_1 = self.main.timer_handler.add_timer(1, 0)
        timer_2 = self.main.timer_handler.add_timer(2, 0)
        timer_3 = self.main.timer_handler.add_timer(4, 0)
        logo_timer = self.main.timer_handler.add_timer(5, 1)
        while self.running:
            # if self.main.timer_handler.check_timer(timer_1):
            #     self.main.state.particles_handler.add_particle(1, 100, 100, 0, 0, 0, 0, 1, 0, 0.5, False, (230, 230, 230), 1, (230, 230, 0), 'add')
            # if self.main.timer_handler.check_timer(timer_2):
            #     self.main.state.particles_handler.add_particle(1, 200, 100, 0, 0, 0, 0, 1, 0, 0.5, False, (230, 230, 230), 1, (230, 0, 230), 'add')
            # if self.main.timer_handler.check_timer(timer_3):
            #     self.main.state.particles_handler.add_particle(1, 300, 100, 0, 0, 0, 0, 1, 0, 0.5, False, (230, 230, 230), 1, (0, 230, 230), 'add')
            if self.main.events_handler.check_key('e', 'pressed') or self.main.timer_handler.check_timer(logo_timer):
                self.main.change_state(state_name='MainMenu')
            if self.running:
                self.update()
                self.draw_game_state()
                self.main.update()

    def update(self):
        self.update_game_state()

    def reset(self, enter):
        self.reset_game_state(enter)
