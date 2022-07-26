from game_state import GameState


class MainMenu(GameState):
    def __init__(self, main):
        super().__init__(main, display=('fade_black', 2, (0, 0, 0), (0, 0)), background=main.state_name,
                         menu=(['Assets/Misc/title.png', 'image'], [{0: ['Start Game', None, 0, 0, False],
                                                                     1: ['Options', None, 0, 0, False],
                                                                     2: ['Extras', None, 0, 0, False],
                                                                     3: ['Quit Game', None, 0, 0, False]}, 0, False, False]))

    def main_loop(self):
        self.running = True
        while self.running:
            if self.main.events_handler.check_key('e', 'pressed'):
                self.main.change_state(state_name='Game')
            if self.main.events_handler.check_key('q', 'pressed'):
                self.main.exit_state_number = 1
            if self.menu.button_triggered:
                self.menu.button_triggered = False
                if self.menu.button_selected == 0:
                    self.main.change_state(state_name='Game')
                if self.menu.button_selected == 1:
                    self.main.change_state(state_name='Options')
                if self.menu.button_selected == 2:
                    self.main.change_state(state_name='Extras')
                if self.menu.button_selected == 3:
                    self.main.change_state(state_name='MainMenuQuit')
            if self.running:
                self.update()
                self.draw_game_state()
                self.main.update()
        self.main.exit_state()

    def update(self):
        self.update_game_state()

    def reset(self, enter):
        self.main.audio_handler.switch_music('main_menu', self.display.transition_time)
        self.reset_game_state(enter)
