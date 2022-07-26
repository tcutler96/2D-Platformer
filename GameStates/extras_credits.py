from game_state import GameState


class ExtrasCredits(GameState):
    def __init__(self, main):
        super().__init__(main, display=('fade_black', 1.5, (0, 0, 0), (0, 0)), background=main.state_name)
        self.credits_list = [['Thanks For Playing', 1, 1],
                             [self.main.game_title, 3, 5],
                             ['', 5, 1],
                             ['^ large gap ^', 1, 10]]
        self.credits_height = self.main.display_size[1] / 8
        self.credits_speed = 10
        self.move = True

    def main_loop(self):
        self.running = True
        while self.running:
            if self.main.controls_handler.check_activity('credits_back'):
                self.main.audio_handler.play_sound('menu_button_click')
                self.main.exit_state_number = 1
            if self.main.controls_handler.check_activity('credits_toggle_scroll'):
                self.toggle_scroll(False)
            if self.main.controls_handler.check_activity('credits_up', 'held'):
                self.manual_scroll(-5, False)
            if self.main.controls_handler.check_activity('credits_down', 'held'):
                self.manual_scroll(5, False)
            if self.main.controls_handler.check_activity('credits_toggle_scroll_mouse'):
                self.toggle_scroll()
            if self.main.controls_handler.check_activity('credits_up_mouse'):
                self.manual_scroll(10)
            if self.main.controls_handler.check_activity('credits_down_mouse'):
                self.manual_scroll(-10)
            if self.running:
                self.update()
                self.draw_game_state()
                self.draw_credits()
                self.main.update()
        self.main.exit_state()

    def update(self):
        self.update_game_state()

    def draw_credits(self):
        # add border to credits such that they don't appear/ disappear at screen edge but fade in almost
        height = 0
        for credit in self.credits_list:
            self.main.font.draw(self.display.display, credit[0], (self.main.display_size[0] // 2, self.main.display_size[1] + self.credits_height + height),
                                self.main.window.menu_colour_1, self.main.window.menu_colour_2, credit[1], credit[2], 'shadow', 1, 'centre')
            height += credit[1] * 15
        if self.move:
            self.credits_height -= self.main.dt * 0.5

    def manual_scroll(self, scroll, mouse=True):
        self.move = False
        self.credits_height += scroll
        if mouse:
            self.display.mouse = True
        else:
            self.display.mouse = False

    def toggle_scroll(self, mouse=True):
        self.move = not self.move
        if mouse:
            self.display.mouse = True
        else:
            self.display.mouse = False

    def reset(self, enter):
        self.credits_height = self.main.display_size[1] / 8
        self.reset_game_state(enter)
