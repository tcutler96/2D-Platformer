import pygame as pg
import sys
from game_state import GameState


class Quit(GameState):
    def __init__(self, main):
        super().__init__(main, display=('fade', 1, (0, 0, 0), (0, 0)))

    def main_loop(self):
        self.running = True
        while self.running:
            self.main.quit_game()
            pg.quit()
            sys.exit()

    def reset(self, enter):
        self.main.audio_handler.switch_music(None, self.display.transition_time)
