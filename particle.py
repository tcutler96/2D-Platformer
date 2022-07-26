import pygame as pg
from math import sqrt


class Particle:
    def __init__(self, main, x_pos, y_pos, x_vel=0, y_vel=0, x_acc=0, y_acc=0, size=1, shrink=0, age_limit=150, mouse_pop=False, colour=(0, 0, 0),
                 glow_size=0, glow_colour=(255, 255, 255), glow_type=None, physics=False, bounce=0.75, collide_objects=True, collide_pop=True):
        self.main = main
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.x_vel = x_vel
        self.y_vel = y_vel
        self.x_acc = x_acc
        self.y_acc = y_acc
        self.size = size
        self.shrink = shrink
        self.colour = colour
        self.age = 0
        if age_limit:
            self.old_age = True
            self.age_limit = age_limit * self.main.fps_base
        else:
            self.old_age = False
            self.age_limit = 0
        self.mouse_pop = mouse_pop
        if glow_size:
            self.glow = True
            if isinstance(glow_size, int):
                self.glow_size = int(glow_size)
                self.glow_pulse = 0
            elif isinstance(glow_size, list):
                self.glow_size = int(glow_size[0])
                self.glow_size_min = self.glow_size
                self.glow_size_max = glow_size[1]
                self.glow_size_step = glow_size[2]
                self.glow_pulse = 1
            self.glow_colour = [glow_colour if glow_colour != (0, 0, 0) else (1, 1, 1)][0]
            if glow_type == 'add':
                self.glow_type = pg.BLEND_RGB_ADD
            elif glow_type == 'sub':
                self.glow_type = pg.BLEND_RGB_SUB
            else:
                self.glow_type = pg.BLEND_ALPHA_SDL2
        else:
            self.glow = False
        self.physics = physics
        self.bounce = min(max(bounce, 0), 1)
        self.collide_objects = collide_objects
        self.collide_pop = collide_pop

    def update(self, tile_rects):
        self.x_pos += self.x_vel
        if self.physics:
            if self.check_collision(tile_rects):
                self.x_vel *= -self.bounce
                self.x_pos += self.x_vel * 2
        self.y_pos += self.y_vel
        if self.physics:
            if self.check_collision(tile_rects):
                self.y_vel *= -self.bounce
                self.y_pos += self.y_vel * 2
        self.x_vel += self.x_acc
        self.y_vel += self.y_acc
        self.size -= self.shrink
        self.age += self.main.dt
        if self.old_age and self.age >= self.age_limit:
            self.size -= 1
        elif self.mouse_pop:
            if sqrt((self.x_pos - self.main.events_handler.mouse_pos[0]) ** 2 + (self.y_pos - self.main.events_handler.mouse_pos[1]) ** 2) < self.size:
                self.pop_particle(True)
        if self.glow:
            if self.glow_pulse == 1:
                self.glow_size += self.glow_size_step
                if self.glow_size >= self.glow_size_max:
                    self.glow_size = self.glow_size_max
                    self.glow_pulse = -1
            elif self.glow_pulse == -1:
                self.glow_size -= self.glow_size_step
                if self.glow_size <= self.glow_size_min:
                    self.glow_size = self.glow_size_min
                    self.glow_pulse = 1

    def check_collision(self, tile_rects):
        particle_rect = pg.Rect(int(self.x_pos), int(self.y_pos), int(self.size), int(self.size))
        for tile_rect in tile_rects:
            if particle_rect.colliderect(tile_rect):
                if self.collide_pop:
                    self.pop_particle()
                return True
        return False

    def draw(self, display):
        # add option to consider display scroll or not
        # if don't consider display scroll then use pos relative to window
        if int(self.size) >= 1:
            if self.glow:
                self.draw_glow(display)
            pg.draw.circle(display.display, self.colour, (int(self.x_pos - display.scroll[0]), int(self.y_pos - display.scroll[1])), int(self.size))

    def draw_glow(self, display):
        glow_radius = int(self.size + self.glow_size)
        glow_surface = pg.Surface((glow_radius * 2, glow_radius * 2))
        pg.draw.circle(glow_surface, self.glow_colour, (glow_radius, glow_radius), glow_radius)
        glow_surface.set_colorkey((0, 0, 0))
        display.display.blit(glow_surface, (int(self.x_pos - display.scroll[0] - glow_radius), int(self.y_pos - display.scroll[1] - glow_radius)), special_flags=self.glow_type)

    def pop_particle(self, sfx=False):
        if sfx:
            self.main.audio_handler.play_sound('particle_pop')
        self.main.state.particles_handler.add_particle(int(self.size * 2), [self.x_pos - self.size / 2, self.x_pos + self.size / 2, 0], [self.y_pos - self.size / 2, self.y_pos + self.size / 2, 0], [-0.5, 0.5, 0], [-0.5, 0.5, 0],
                                                       self.x_acc, self.y_acc, [self.size / 4, self.size / 2, 0], [0.025, 0.075, 0], 0, False, self.colour, 1, self.glow_colour, self.glow_type)
        self.size = 0
