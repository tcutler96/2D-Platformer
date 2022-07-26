from particle import Particle
import random


class ParticleHandler:
    def __init__(self, main):
        self.main = main
        self.particles = []

    def add_particle(self, amount=1, x_pos=0, y_pos=0, x_vel=0, y_vel=0, x_acc=0, y_acc=0, size=1, shrink=0, age_limit=150, mouse_pop=False,
                     colour=(0, 0, 0), glow_size=0, glow_colour=(255, 255, 255), glow_type=None, physics=False, bounce=0.75, collide_pop=True, collide_objects=True):
        for _ in range(amount):
            self.particles.append(Particle(self.main, self.get_value(x_pos), self.get_value(y_pos), self.get_value(x_vel), self.get_value(y_vel), self.get_value(x_acc), self.get_value(y_acc), self.get_value(size),
                                           self.get_value(shrink),  self.get_value(age_limit), mouse_pop, self.get_value(colour), glow_size, self.get_value(glow_colour), glow_type,
                                           physics, self.get_value(bounce), collide_objects, collide_pop))

    def get_value(self, input):
        if isinstance(input, list):
            if input[2] == 0:
                value = random.uniform(input[0] if input[0] < input[1] else input[1], input[0] if input[0] > input[1] else input[1])
            else:
                value = random.randint(input[0] if input[0] < input[1] else input[1], input[0] if input[0] > input[1] else input[1])
        elif isinstance(input, tuple):
            value = list(input)
            for index, val in enumerate(value):
                if isinstance(val, list):
                    value[index] = random.randint(val[0], val[1])
            value = tuple(value)
        else:
            value = input
        return value

    def update(self, display, tile_rects, game_objects):
        for _, particle in sorted(enumerate(self.particles), reverse=True):
            # add option to collide with player rect... bubbles spawn by game should pop when hitting player...
            if particle.collide_objects:
                for game_object in game_objects:
                    tile_rects.append(game_object.collide_rect)
            particle.update(tile_rects)
            # add option to pop particle when it gets too old...
            if particle.size < 1 or (not -display.display_size[0] / 2 + display.scroll[0] < particle.x_pos < 1.5 * display.display_size[0] + display.scroll[0]) or \
                    (not -display.display_size[1] / 2 + display.scroll[1] < particle.y_pos < 1.5 * display.display_size[1] + display.scroll[1]):
                self.particles.remove(particle)

    def draw(self, display):
        # which order do we to draw particles in, oldest or newest first?
        for _, particle in sorted(enumerate(self.particles), reverse=True):
            particle.draw(display)


