import pygame as pg


class MenuButton:
    def __init__(self, main, button_type, text, position, colour_1, colour_2, scale, spacing, width, height, debug_colour):
        self.main = main
        self.button_type = button_type
        self.text = text
        self.pos_x = position[0]
        self.pos_y = position[1]
        self.colour_1 = colour_1
        self.colour_2 = colour_2
        self.scale = scale
        self.spacing = spacing
        self.width = width
        self.height = height
        self.debug_colour = debug_colour
        self.rect = pg.Rect(self.pos_x - 1 - self.width / 2, self.pos_y - 1, self.width + 2, self.height + 2)
        self.collide = False

    def draw(self, display, selected):
        if self.main.debug_mode:
            pg.draw.rect(display.display, self.debug_colour, self.rect, not selected)
        if self.button_type == 'simple':
            self.main.font.draw(display.display, self.text, (self.pos_x, self.pos_y), self.colour_1, self.colour_2, self.scale, self.spacing, ['shadow' if selected else 'none'][0], 1, 'centre')
        elif self.button_type == 'scroll':
            self.main.font.draw(display.display, self.text[0], (self.pos_x - self.width / 2, self.pos_y), self.colour_1,
                                self.colour_2, self.scale, self.spacing, ['shadow' if selected else 'none'][0], 1, 'left')
            self.main.font.draw(display.display, self.text[1], (self.pos_x + self.width / 2, self.pos_y), self.colour_1,
                                self.colour_2, self.scale, self.spacing, ['shadow' if selected else 'none'][0], 1, 'right')
        elif self.button_type == 'input':
            self.main.font.draw(display.display, self.text[0], (self.pos_x - self.width / 2, self.pos_y), self.colour_1,
                                self.colour_2, self.scale, self.spacing, ['shadow' if selected else 'none'][0], 1, 'left')
            if 'controller' in self.text[1] and self.text[1].split(' ')[0] in self.main.controls_handler.controller_buttons:
                icon = self.main.controls_handler.controller_buttons[self.text[1].split(' ')[0]][1]
                display.display.blit(icon, (self.pos_x + self.width // 2 - icon.get_width() - 12, self.pos_y + 1))
                if selected:
                    self.main.font.draw(display.display, '  <', (self.pos_x + self.width / 2, self.pos_y), self.colour_1,
                                        self.colour_2, self.scale, self.spacing, ['shadow' if selected else 'none'][0], 1, 'right')
            else:
                self.main.font.draw(display.display, self.text[1], (self.pos_x + self.width / 2, self.pos_y), self.colour_1,
                                    self.colour_2, self.scale, self.spacing, ['shadow' if selected else 'none'][0], 1, 'right')

    def update(self):
        if self.rect.collidepoint(self.main.events_handler.mouse_pos):
            self.collide = True
        else:
            self.collide = False
