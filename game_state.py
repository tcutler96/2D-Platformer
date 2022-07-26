from display import Display
from background import Background
from tile_map import TileMap
from game_object import GameObject
from player import Player
from menu import Menu
from particle_handler import ParticleHandler


class GameState:
    def __init__(self, main, display=('instant', 0, (0, 0, 0), (0, 0), True, False), background=None, tile_map=None, game_objects=None, player=None, menu=None):
        self.main = main
        self.state_name = self.main.state_name
        self.display = Display(main=self.main, transition_type=display[0], transition_time=display[1], scroll=display[2], scroll_offset=display[3])
        self.background = Background(main=self.main, theme=background)
        self.tile_map = TileMap(main=self.main) if tile_map else None
        self.game_objects = [GameObject(main=self.main, name=game_object[0], position=game_object[1]) for game_object in game_objects] if game_objects else []
        self.player = Player(main=self.main, position=self.tile_map.spawn_point if self.tile_map else (0, 0)) if player else None
        self.menu = Menu(main=self.main, title_data=menu[0], button_data=menu[1], reset_background=[False if background else True][0]) if menu else None
        self.particles_handler = ParticleHandler(main=self.main)
        self.running = False

    def update_game_state(self):
        if self.tile_map:
            self.tile_map.update()
        if self.game_objects:
            for game_object in self.game_objects:
                game_object.update()
        if self.player:
            self.player.update_player(self.tile_map.tile_rects, self.game_objects)
        if self.particles_handler:
            self.particles_handler.update(self.display, self.tile_map.tile_rects if self.tile_map else [], self.game_objects if self.game_objects else [])
        if self.menu:
            self.menu.update()

    def draw_game_state(self):
        self.display.draw(self)

    def reset_game_state(self, enter):
        self.update_game_state()
        if self.menu:
            self.menu.reset(enter)
        self.draw_game_state()
