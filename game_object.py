import pygame as pg


class GameObject:
    # object name as folder name, state folder name format 'order_name', image name format 'order_frame length', fill empty space with (255, 255, 255)
    def __init__(self, main, name, position, track_player_collision=True, flip_h=False, flip_v=False):
        self.main = main
        self.name = name
        self.tile_size = self.main.tile_size
        self.path = 'Assets/Objects/'
        self.outline_colour = (255, 255, 255)
        self.debug_colour_1 = (225, 0, 175)
        self.debug_colour_2 = (127, 255, 212)
        self.debug_colour_3 = (97, 4, 143)
        self.pos_x = position[0]
        self.pos_y = position[1]
        self.data, self.states, self.states_dir = self.get_data()
        self.track_player_collision = track_player_collision
        self.flip_h = flip_h
        self.flip_v = flip_v
        self.frame = 0
        self.loops = 0
        self.state = self.states[0]
        self.sprites_data, self.sprite_order = self.load()
        self.sprite_data = self.sprites_data[self.sprite_order[self.state][self.frame]]
        self.sprite_image, self.sprite_width, self.sprite_height, self.sprite_mask, self.sprite_outline, self.sprite_debug_outline = \
            None, self.sprite_data[0][1], self.sprite_data[0][2], None, None, None
        self.collide_rect_width, self.collide_rect_height = None, None
        self.collide_rect_pos1 = [[self.sprite_data[1][0][0] if not self.flip_h else self.sprite_width - self.sprite_data[1][1][0] - 1][0],
                                  [self.sprite_data[1][0][1] if not self.flip_v else self.sprite_height - self.sprite_data[1][1][1] - 1][0]]
        self.collide_rect_pos2 = [[self.sprite_data[1][1][0] if not self.flip_h else self.sprite_width - self.sprite_data[1][0][0] - 1][0],
                                  [self.sprite_data[1][1][1] if not self.flip_v else self.sprite_height - self.sprite_data[1][0][1] - 1][0]]
        self.collide_rect_align = [[self.collide_rect_pos2[0] if not self.flip_h else self.collide_rect_pos1[0]][0], [self.collide_rect_pos2[1] if not self.flip_v else self.collide_rect_pos1[1]][0]]
        self.flip = [self.flip_h, self.flip_v]
        self.update_sprite()
        self.sprite_rect = self.get_rect()
        self.collide_rect = self.get_rect(True)
        self.player_collision = False
        self.player_collision_pos = None
        self.clean_name = ' '.join([word for word in self.name.split('_')])

    def get_data(self):
        states_dir = self.main.helper.get_files(self.path + self.name)
        states = []
        data = {}
        for state_dir in states_dir:
            state = state_dir.split('_')[1]
            states.append(state)
            frames = []
            data[state] = []
            for file in self.main.helper.get_files(self.path + self.name + '/' + state_dir, 'png'):
                file_name = file[:-4].split('_')
                frames.append(int(file_name[1]))
                data[state].append([file, frames[-1]])
        return data, states, states_dir

    def load(self):
        sprites_data = {}
        sprite_order = {}
        for state, state_dir in zip(self.data, self.states_dir):
            sprite_data = []
            for index, frame in enumerate(self.data[state]):
                sprite_id = state + str(index)
                sprite_image = self.main.helper.load_image('Assets/Objects/' + self.name + '/' + state_dir + '/' + frame[0])
                sprite_width, sprite_height = sprite_image.get_size()
                sprite_coords = [(x, y) for x in range(sprite_width) for y in range(sprite_height)]
                collide_rect_pos1 = (0, 0)
                for coord in sprite_coords:
                    if sprite_image.get_at(coord)[0:-1] == (255, 0, 0):
                        collide_rect_pos1 = coord
                        sprite_image.set_at(coord, (255, 255, 255, 0))
                        break
                collide_rect_pos2 = (sprite_width - 1, sprite_height - 1)
                if collide_rect_pos1 != (0, 0):
                    for coord in sprite_coords[::-1]:
                        if sprite_image.get_at(coord)[0:-1] == (0, 0, 255):
                            collide_rect_pos2 = coord
                            sprite_image.set_at(coord, (255, 255, 255, 0))
                            break
                sprite_outline = self.main.helper.outline_image(sprite_image, False, outline_style='full', outline_size=1, outline_colour=self.outline_colour)
                sprite_debug_outline = self.main.helper.outline_image(sprite_image, False, outline_style='full', outline_size=0, outline_colour=self.debug_colour_1)
                collide_rect_width = collide_rect_pos2[0] - collide_rect_pos1[0] + 1
                collide_rect_height = collide_rect_pos2[1] - collide_rect_pos1[1] + 1
                sprites_data[sprite_id] = [[sprite_image, sprite_width, sprite_height, sprite_outline, sprite_debug_outline],
                                           [list(collide_rect_pos1), list(collide_rect_pos2), collide_rect_width, collide_rect_height]]
                for _ in range(frame[1]):
                    sprite_data.append(sprite_id)
            sprite_order[state] = sprite_data
        return sprites_data, sprite_order

    def place(self, position, centre=True):
        self.pos_x = position[0] * self.tile_size
        self.pos_y = position[1] * self.tile_size
        if centre:
            self.pos_x += (self.tile_size - self.sprite_width) // 2
            self.pos_y += (self.tile_size - self.sprite_height) // 2

    def get_rect(self, collide_rect=False, scroll=None):
        if collide_rect:
            return pg.Rect(self.pos_x + self.collide_rect_pos1[0] - [scroll[0] if scroll else 0][0], self.pos_y + self.collide_rect_pos1[1] - [scroll[1] if scroll else 0][0],
                           self.collide_rect_width, self.collide_rect_height)
        else:
            return pg.Rect(self.pos_x - [scroll[0] if scroll else 0][0], self.pos_y - [scroll[1] if scroll else 0][0], self.sprite_width, self.sprite_height)

    def change_state(self, state):
        if self.state != state and state in self.states:
            self.state = state
            self.frame = -1
            self.loops = 0
            self.update_sprite()

    def update(self):
        self.update_frame()

    def update_frame(self):
        self.frame += int(self.main.dt)
        if self.frame >= len(self.sprite_order[self.state]):
            self.frame = 0
            self.loops += 1
        self.update_sprite()

    # noinspection PyTypeChecker
    def update_sprite(self):
        self.sprite_data = self.sprites_data[self.sprite_order[self.state][self.frame]]
        self.sprite_image = pg.transform.flip(self.sprite_data[0][0], self.flip_h, self.flip_v)
        self.sprite_mask = pg.mask.from_surface(self.sprite_image)
        old_width, old_height = self.sprite_width, self.sprite_height
        self.sprite_width = self.sprite_data[0][1]
        self.sprite_height = self.sprite_data[0][2]
        self.sprite_outline = pg.transform.flip(self.sprite_data[0][3], self.flip_h, self.flip_v)
        self.sprite_debug_outline = pg.transform.flip(self.sprite_data[0][4], self.flip_h, self.flip_v)
        self.collide_rect_width = self.sprite_data[1][2]
        self.collide_rect_height = self.sprite_data[1][3]
        self.collide_rect_pos1 = [[self.sprite_data[1][0][0] if not self.flip_h else self.sprite_width - self.sprite_data[1][1][0] - 1][0],
                                  [self.sprite_data[1][0][1] if not self.flip_v else self.sprite_height - self.sprite_data[1][1][1] - 1][0]]
        self.collide_rect_pos2 = [[self.sprite_data[1][1][0] if not self.flip_h else self.sprite_width - self.sprite_data[1][0][0] - 1][0],
                                  [self.sprite_data[1][1][1] if not self.flip_v else self.sprite_height - self.sprite_data[1][0][1] - 1][0]]
        old_align = [[self.collide_rect_align[0] if self.flip_h == self.flip[0] else old_width - self.collide_rect_align[0] - 1][0],
                     [self.collide_rect_align[1] if self.flip_v == self.flip[1] else old_height - self.collide_rect_align[1] - 1][0]]
        self.collide_rect_align = [[self.collide_rect_pos2[0] if not self.flip_h else self.collide_rect_pos1[0]][0], [self.collide_rect_pos2[1] if not self.flip_v else self.collide_rect_pos1[1]][0]]
        self.pos_x += old_align[0] - self.collide_rect_align[0]
        self.pos_y += old_align[1] - self.collide_rect_align[1]
        self.flip = [self.flip_h, self.flip_v]

    def draw(self, display):
        if self.player_collision:
            self.highlight(display)
        display.display.blit(self.sprite_image, (self.pos_x - display.scroll[0], self.pos_y - display.scroll[1]))
        if display.main.debug_mode:
            self.draw_debug(display)

    def highlight(self, display):
        display.display.blit(self.sprite_outline, (self.pos_x - display.scroll[0] - 1, self.pos_y - display.scroll[1] - 1))
        self.main.state.particles_handler.add_particle(1, [self.pos_x, self.pos_x + self.sprite_width, 1], [self.pos_y - 2, self.pos_y - 10, 1], 0, [-0.5, 0, 0], 0, 0,
                                                       [0, 1, 1], 0, 0.25, None, (230, 230, 230), [1, 3, 0.5], ([0, 50], [0, 25], [0, 100]), 'add')

    def draw_debug(self, display):
        display.display.blit(self.sprite_debug_outline, (self.pos_x - display.scroll[0], self.pos_y - display.scroll[1]))
        pg.draw.rect(display.display, self.debug_colour_2, self.get_rect(True, display.scroll), 1)
        # pg.draw.rect(display.display, self.debug_colour_3, self.get_rect(False, display.scroll), 1)

    def interact(self):
        print(self.name)
