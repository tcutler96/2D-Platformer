import pygame as pg
from tile_map_chunk import TileMapChunk
from random import randint


class TileMap:
    # map types: Text/ Text2 (load from text file), Flat (flat ground), Hills (random noise hills), Sine (sine wave hills), Empty (no tiles)
    def __init__(self, main):
        self.main = main
        self.chunk_size = self.main.chunk_size
        self.tile_size = self.main.tile_size
        self.path = 'Assets/Tiles/'
        self.debug_colour_1 = (106, 90, 205)
        self.debug_colour_2 = (112, 128, 144)
        self.debug_colour_3 = (0, 225, 175)
        self.tile_dict = self.load_tiles()
        self.random_tiles = True
        # create function to find suitable spawn point, start with chunk (0, 0) and loop through tiles to find one that has 2 empty spaces above it...
        # need to call function/ determine spawn point after some chunks have been generated of course
        # set spawn point to horizontal centre of block
        # set player horizontal direction according to whether there are other tiles to the left or right
        self.spawn_point = (55, 50)
        self.tile_map = {}
        self.tiles = []
        self.chunks = []
        self.tile_rects = []
        # play around with values...
        self.noise_scale = 0.1
        self.noise_octaves = 6
        self.noise_persistence = 0.5
        self.noise_lacunarity = 2
        self.noise_threshold = 0
        self.noise_clean = 3
        self.noise_fill = 6
        self.noise_remove = 2
        self.noise_offset_x = 0  # randint(-99999, 99999)
        self.noise_offset_y = 0  # randint(-99999, 99999)

    def load_tiles(self):
        tile_dict = {}
        for file_name in self.main.helper.get_files(self.path, 'png'):
            tile_sprite = self.main.helper.load_image(self.path + file_name)
            file_name = file_name[:-4].split('_')
            tile_name = file_name[0]
            tile_prob = float(file_name[2])
            tile_data = [[tile_sprite], [tile_prob]]
            if tile_name not in tile_dict:
                tile_dict[tile_name] = tile_data
            else:
                tile_dict[tile_name] = [i + j for i, j in zip(tile_dict[tile_name], tile_data)]
        return tile_dict

    def update_chunks(self):
        self.chunks = []
        for y in range(-1, int(self.main.display_size[1] / (self.chunk_size * self.tile_size)) + 1):
            for x in range(-1, int(self.main.display_size[0] / (self.chunk_size * self.tile_size)) + 1):
                self.chunks.append((x + int(round(self.main.state.display.scroll[0] / (self.chunk_size * self.tile_size))), y + int(round(self.main.state.display.scroll[1] / (self.chunk_size * self.tile_size)))))

    def update(self):
        self.update_chunks()
        self.tile_rects = []
        for chunk in self.chunks:
            if chunk not in self.tile_map:
                self.tile_map[chunk] = TileMapChunk(self, chunk)
            self.tile_rects = self.tile_map[chunk].update(self.tile_rects)

    def draw(self, display):
        for chunk in self.chunks:
            self.tile_map[chunk].draw(display)
        if display.main.debug_mode:
            pg.draw.rect(display.display, self.debug_colour_3, pg.Rect(-5 - display.scroll[0], -1 - display.scroll[1], 10, 2), 1)
            pg.draw.rect(display.display, self.debug_colour_3, pg.Rect(-1 - display.scroll[0], -5 - display.scroll[1], 2, 10), 1)
