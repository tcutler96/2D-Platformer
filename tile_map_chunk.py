import pygame as pg
import numpy as np
import random
from noise import snoise2


class TileMapChunk:
    def __init__(self, tile_map, chunk_pos):
        self.tile_map = tile_map.tile_map
        self.chunk_pos = chunk_pos
        self.chunk_size = tile_map.chunk_size
        self.tile_size = tile_map.tile_size
        self.tile_dict = tile_map.tile_dict
        self.random_tiles = tile_map.random_tiles
        self.debug_colour_1 = tile_map.debug_colour_1
        self.debug_colour_2 = tile_map.debug_colour_2
        self.noise_scale = tile_map.noise_scale
        self.noise_octaves = tile_map.noise_octaves
        self.noise_persistence = tile_map.noise_persistence
        self.noise_lacunarity = tile_map.noise_lacunarity
        self.noise_threshold = tile_map.noise_threshold
        self.noise_clean = tile_map.noise_clean
        self.noise_fill = tile_map.noise_fill
        self.noise_remove = tile_map.noise_remove
        self.noise_offset_x = tile_map.noise_offset_x
        self.noise_offset_y = tile_map.noise_offset_y
        self.chunk_data = {}
        self.tile_positions = []
        self.generate_chunk()

    def generate_chunk(self):
        self.generate_noise()
        self.clean_noise()
        self.create_tiles()

    def generate_noise(self):
        for y in range(self.chunk_size):
            for x in range(self.chunk_size):
                true_x = self.chunk_pos[0] * self.chunk_size + x
                true_y = self.chunk_pos[1] * self.chunk_size + y
                self.add_tile_data(true_x, true_y)

    def add_tile_data(self, x, y):
        self.chunk_data[(x, y)] = [self.calculate_noise(x, y)]
        self.chunk_data[(x, y)].append(self.chunk_data[(x, y)][0] > self.noise_threshold)

    def calculate_noise(self, x, y):
        return snoise2((x + self.noise_offset_x) * self.noise_scale, (y + self.noise_offset_y) * self.noise_scale, octaves=self.noise_octaves,
                       persistence=self.noise_persistence, lacunarity=self.noise_lacunarity, repeatx=1024, repeaty=1024)

    def clean_noise(self):
        clean = True
        while self.noise_clean and clean:
            self.noise_clean -= 1
            clean = False
            for tile_pos, tile_data in self.chunk_data.items():
                _, surround_sum, edge_tiles = self.get_surround(tile_pos)
                if tile_data[1]:
                    if surround_sum <= self.noise_remove:
                        tile_data[1] = False
                        clean = True
                else:
                    if surround_sum >= self.noise_fill:
                        tile_data[1] = True
                        clean = True
                if clean and edge_tiles:
                    self.update_edge_tile(edge_tiles)

    def get_surround(self, tile_pos,):
        tile_chunk = (tile_pos[0] // self.chunk_size, tile_pos[1] // self.chunk_size)
        surround = np.zeros((3, 3))
        surround_sum = 0
        edge_tiles = []
        for surround_y in range(tile_pos[1] - 1, tile_pos[1] + 2):
            for surround_x in range(tile_pos[0] - 1, tile_pos[0] + 2):
                array_x = surround_x - tile_pos[0] + 1
                array_y = surround_y - tile_pos[1] + 1
                surround_chunk = tile_chunk
                if surround_x // self.chunk_size < tile_pos[0] // self.chunk_size:
                    surround_chunk = (surround_chunk[0] - 1, surround_chunk[1])
                elif surround_x // self.chunk_size > tile_pos[0] // self.chunk_size:
                    surround_chunk = (surround_chunk[0] + 1, surround_chunk[1])
                if surround_y // self.chunk_size < tile_pos[1] // self.chunk_size:
                    surround_chunk = (surround_chunk[0], surround_chunk[1] - 1)
                elif surround_y // self.chunk_size > tile_pos[1] // self.chunk_size:
                    surround_chunk = (surround_chunk[0], surround_chunk[1] + 1)
                if surround_chunk == self.chunk_pos:
                    if (surround_x, surround_y) not in self.chunk_data:
                        self.add_tile_data(surround_x, surround_y)
                    if self.chunk_data[(surround_x, surround_y)][1]:
                        surround[array_y, array_x] = 1
                        surround_sum += 1
                elif surround_chunk in self.tile_map:
                    if self.tile_map[surround_chunk].chunk_data[(surround_x, surround_y)][1]:
                        surround[array_y, array_x] = 1
                        surround_sum += 1
                        edge_tiles.append((surround_x, surround_y))
                elif self.calculate_noise(surround_x, surround_y) > self.noise_threshold:
                    surround[array_y, array_x] = 1
                    surround_sum += 1
        return surround, surround_sum, edge_tiles

    def update_edge_tile(self, edge_tiles):
        for edge_tile in edge_tiles:
            surround, _, _ = self.get_surround(edge_tile)
            self.tile_map[(edge_tile[0] // self.chunk_size, edge_tile[1] // self.chunk_size)].chunk_data[(edge_tile[0], edge_tile[1])][2] = self.create_tile(surround)

    def create_tiles(self):
        for tile_pos, tile_data in self.chunk_data.items():
            if tile_data[1]:
                self.tile_positions.append(tile_pos)
                surround, _, _ = self.get_surround(tile_pos)
                tile_data.append(self.create_tile(surround))
                tile_data.append(pg.Rect(tile_pos[0] * self.tile_size, tile_pos[1] * self.tile_size, self.tile_size, self.tile_size))

    def create_tile(self, surround):
        surface = pg.Surface((self.tile_size, self.tile_size))
        surface.fill((255, 255, 255))
        surface.set_colorkey((255, 255, 255))
        # tile centre
        self.blit_tile_piece(surface, 'inner', (5, 5), random.randint(0, 3))
        # top edge
        if surround[0, 1]:
            self.blit_tile_piece(surface, 'innerh', (5, 0))
        else:
            self.blit_tile_piece(surface, 'outert', (5, 0))
        # bottom edge
        if surround[2, 1]:
            self.blit_tile_piece(surface, 'innerh', (5, self.tile_size - 5))
        else:
            self.blit_tile_piece(surface, 'outerb', (5, self.tile_size - 5))
        # left edge
        if surround[1, 0]:
            self.blit_tile_piece(surface, 'innerh', (0, 5), 1)
        else:
            self.blit_tile_piece(surface, 'outerv', (0, 5))
        # right edge
        if surround[1, 2]:
            self.blit_tile_piece(surface, 'innerh', (self.tile_size - 5, 5), 1)
        else:
            self.blit_tile_piece(surface, 'outerv', (self.tile_size - 5, 5), 2)
        # top left corner
        if not surround[0, 1] and not surround[1, 0]:
            self.blit_tile_piece(surface, 'outerc1', (0, 0))
        elif surround[0, 1] and not surround[1, 0]:
            self.blit_tile_piece(surface, 'outerc2', (0, 0), 1)
        elif not surround[0, 1] and surround[1, 0]:
            self.blit_tile_piece(surface, 'outerc2', (0, 0))
        else:
            if surround[0, 0]:
                self.blit_tile_piece(surface, 'innerc1', (0, 0))
            else:
                self.blit_tile_piece(surface, 'innerc2', (0, 0))
        # top right corner
        if not surround[0, 1] and not surround[1, 2]:
            self.blit_tile_piece(surface, 'outerc1', (self.tile_size - 5, 0), 3)
        elif surround[0, 1] and not surround[1, 2]:
            self.blit_tile_piece(surface, 'outerc2', (self.tile_size - 5, 0), 3)
        elif not surround[0, 1] and surround[1, 2]:
            self.blit_tile_piece(surface, 'outerc2', (self.tile_size - 5, 0))
        else:
            if surround[0, 2]:
                self.blit_tile_piece(surface, 'innerc1', (self.tile_size - 5, 0))
            else:
                self.blit_tile_piece(surface, 'innerc2', (self.tile_size - 5, 0), 3)
        # bot left corner
        if not surround[2, 1] and not surround[1, 0]:
            self.blit_tile_piece(surface, 'outerc1', (0, self.tile_size - 5), 1)
        elif surround[2, 1] and not surround[1, 0]:
            self.blit_tile_piece(surface, 'outerc2', (0, self.tile_size - 5), 1)
        elif not surround[2, 1] and surround[1, 0]:
            self.blit_tile_piece(surface, 'outerc2', (0, self.tile_size - 5), 2)
        else:
            if surround[2, 0]:
                self.blit_tile_piece(surface, 'innerc1', (0, self.tile_size - 5))
            else:
                self.blit_tile_piece(surface, 'innerc2', (0, self.tile_size - 5), 1)
        # bot right corner
        if not surround[2, 1] and not surround[1, 2]:
            self.blit_tile_piece(surface, 'outerc1', (self.tile_size - 5, self.tile_size - 5), 2)
        elif surround[2, 1] and not surround[1, 2]:
            self.blit_tile_piece(surface, 'outerc2', (self.tile_size - 5, self.tile_size - 5), 3)
        elif not surround[2, 1] and surround[1, 2]:
            self.blit_tile_piece(surface, 'outerc2', (self.tile_size - 5, self.tile_size - 5), 2)
        else:
            if surround[2, 2]:
                self.blit_tile_piece(surface, 'innerc1', (self.tile_size - 5, self.tile_size - 5))
            else:
                self.blit_tile_piece(surface, 'innerc2', (self.tile_size - 5, self.tile_size - 5), 2)
        return surface

    def blit_tile_piece(self, surface, tile_piece, location, rotation=0):
        return surface.blit(pg.transform.rotate(self.choose_tile_piece(f'{tile_piece}'), rotation * 90), location)

    def choose_tile_piece(self, tile_piece):
        if self.random_tiles:
            tile_piece_choice = random.choices(range(len(self.tile_dict[tile_piece][0])), self.tile_dict[tile_piece][1])[0]
        else:
            tile_piece_choice = 0
        return self.tile_dict[tile_piece][0][tile_piece_choice].copy()

    def update(self, tile_rects):
        for tile_pos in self.tile_positions:
            tile_data = self.chunk_data[tile_pos]
            tile_rects.append(tile_data[3])
        return tile_rects

    def draw(self, display):
        for tile_pos in self.tile_positions:
            tile_data = self.chunk_data[tile_pos]
            display.display.blit(tile_data[2], (tile_pos[0] * self.tile_size - display.scroll[0], tile_pos[1] * self.tile_size - display.scroll[1]))
            if display.main.debug_mode:
                pg.draw.rect(display.display, self.debug_colour_2, pg.Rect(tile_pos[0] * self.tile_size - display.scroll[0],
                                                                           tile_pos[1] * self.tile_size - display.scroll[1], self.tile_size, self.tile_size), 1)
        if display.main.debug_mode:
            pg.draw.rect(display.display, self.debug_colour_1, pg.Rect(self.chunk_pos[0] * self.chunk_size * self.tile_size - display.scroll[0],
                                                                       self.chunk_pos[1] * self.chunk_size * self.tile_size - display.scroll[1],
                                                                       self.chunk_size * self.tile_size, self.chunk_size * self.tile_size), 1)
