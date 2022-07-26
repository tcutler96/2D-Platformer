import pygame as pg


class Font:
    def __init__(self, main):
        self.main = main
        self.path = 'Assets/Misc/font_characters.png'
        self.character_order = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'a', 'b', 'c', 'd', 'e', 'f', 'g',
                                'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '.', ',', '\'', '"',
                                '?', '!', '@', '_', '*', '#', '$', '%', '&', '(', ')', '[', ']', '{', '}', '<', '>', '+', '-', '=', '/', '\\', ':', ';', '^', '|', '~', ' ']
        self.colour_1 = (0, 0, 0)
        self.colour_2 = (255, 255, 255)
        self.font_image = self.main.helper.load_image(self.path, None)
        self.font_image_width, self.font_image_height = self.font_image.get_width(), self.font_image.get_height()
        self.characters = self.split_characters()

    def split_characters(self):
        characters = {}
        character_width = 0
        character_count = 0
        for x in range(self.font_image_width):
            if self.font_image.get_at((x, 0))[0:-1] == (255, 0, 0):
                character_image = self.clip(x - character_width, character_width)
                characters[self.character_order[character_count]] = [character_image.copy(), character_width]
                character_count += 1
                character_width = 0
            else:
                character_width += 1
        return characters

    def clip(self, x, width):
        handle_surf = self.font_image.copy()
        clip_rect = pg.Rect(x, 0, width, self.font_image_height)
        handle_surf.set_clip(clip_rect)
        image = self.font_image.subsurface(handle_surf.get_clip())
        return image.copy()

    def get_width(self, text, spacing=1):
        font_width = 0
        for character in text:
            font_width += self.characters[character][1] + spacing
        return font_width

    def draw(self, display, text, position, colour=(255, 255, 255), outline=(0, 0, 0), scale=1, spacing=1, outline_style=None, outline_size=1, h_align=None, v_align=None):
        font_width = self.get_width(text, spacing)
        scale = int(scale)
        if h_align == 'centre':
            x_offset = scale * (-font_width + 1.5 * spacing) // 2
        elif h_align == 'right':
            x_offset = scale * (-font_width + 1)
        else:
            x_offset = 0
        if v_align == 'middle':
            y_offset = scale * -self.font_image_height // 2
        elif v_align == 'bottom':
            y_offset = scale * -self.font_image_height + 1
        else:
            y_offset = 0
        if colour == self.colour_1:
            colour = (1, 1, 1)
        elif colour == self.colour_2:
            colour = (254, 254, 254)
        if outline == self.colour_1:
            outline = (1, 1, 1)
        elif outline == self.colour_2:
            outline = (254, 254, 254)
        for character in text:
            char_image = self.characters[character][0].copy()
            char_width = self.characters[character][1] * scale
            char_height = self.font_image_height * scale
            char_image = pg.transform.scale(char_image, (char_width, char_height))
            char_image = self.main.helper.palette_swap(char_image, self.colour_1, colour)
            char_image.set_colorkey(self.colour_2)
            display.blit(self.main.helper.outline_image(char_image, outline_style=outline_style, outline_size=outline_size, outline_colour=outline),
                         (position[0] + x_offset - 1, position[1] + y_offset - 1))
            x_offset += char_width + scale * spacing
