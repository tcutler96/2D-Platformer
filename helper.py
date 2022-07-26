import pygame as pg
import os


class Helper:
    def __init__(self, main):
        self.main = main

    # gets all files in path with given extension
    def get_files(self, path, extension=None):
        if extension:
            return [f for f in os.listdir(path) if f.endswith('.' + extension)]
        else:
            return [f for f in os.listdir(path)]

    # loads image from given path
    def load_image(self, path, colour_key=(255, 255, 255)):
        image = pg.image.load(path).convert()
        if colour_key:
            image.set_colorkey(colour_key)
        return image

    # swaps one colour in an image for another
    def palette_swap(self, image, old_colour, new_colour):
        new_image = pg.Surface(image.get_size())
        new_image.fill(new_colour)
        old_image = image.copy()
        old_image.set_colorkey(old_colour)
        new_image.blit(old_image, (0, 0))
        return new_image

    # draws outline around image with given style and colour
    def outline_image(self, image, blit_image=True, display=None, pos=None, outline_style='shadow', outline_size=1, outline_colour=(0, 0, 0), edge_every=1):
        if isinstance(image, str):
            image = self.load_image(image)
        offsets, blit_image, outline_size, trim = self.get_outline_data(blit_image, outline_style, int(outline_size))
        if not display:
            display = pg.Surface((image.get_width() + outline_size * 2, image.get_height() + outline_size * 2))
            display.fill((0, 0, 0))
            display.set_colorkey((0, 0, 0))
            pos = (outline_size, outline_size)
        if blit_image == 'first':
            display.blit(image, (pos[0], pos[1]))
        if offsets:
            display = self.blit_outline(image, display, pos, outline_colour, offsets, edge_every)
        if blit_image == 'last':
            display.blit(image, (pos[0], pos[1]))
        display = self.trim_outline(display, outline_size, trim)
        return display

    # gets data of given outline style
    def get_outline_data(self, blit_image, outline_style, outline_size):
        if blit_image:
            blit_image = 'last'
        if outline_style == 'full':
            if outline_size == 0 and blit_image:
                blit_image = 'first'
            offsets = [[x - outline_size, y - outline_size] for x in range(outline_size * 2 + 1) for y in range(outline_size * 2 + 1)]
            trim = [0, 0, 0, 0]
        elif outline_style in ['shadow', 'shadow_bl']:
            offsets = [[x - outline_size, y] for x in range(outline_size + 1) for y in range(outline_size + 1)]
            trim = [0, 1, 1, 0]
        elif outline_style == 'shadow_tl':
            offsets = [[x - outline_size, y - outline_size] for x in range(outline_size + 1) for y in range(outline_size + 1)]
            trim = [0, 1, 0, 1]
        elif outline_style == 'shadow_tr':
            offsets = [[x, y - outline_size] for x in range(outline_size + 1) for y in range(outline_size + 1)]
            trim = [1, 0, 0, 1]
        elif outline_style == 'shadow_br':
            offsets = [[x, y] for x in range(outline_size + 1) for y in range(outline_size + 1)]
            trim = [1, 0, 1, 0]
        elif outline_style == 'sides':
            offsets = [[x - outline_size, y - outline_size] for x in range(outline_size * 2 + 1) for y in range(outline_size * 2 + 1)
                       if not (abs(x - outline_size) == outline_size & abs(y - outline_size) == outline_size)]
            trim = [0, 0, 0, 0]
        elif outline_style == 'left':
            offsets = [[x - outline_size, 0] for x in range(outline_size + 1)]
            trim = [0, 1, 1, 1]
        elif outline_style == 'right':
            offsets = [[x, 0] for x in range(outline_size + 1)]
            trim = [1, 0, 1, 1]
        elif outline_style == 'top':
            offsets = [[0, y - outline_size] for y in range(outline_size + 1)]
            trim = [1, 1, 0, 1]
        elif outline_style == 'bottom':
            offsets = [[0, y]for y in range(outline_size + 1)]
            trim = [1, 1, 1, 0]
        else:
            outline_size = 0
            blit_image = 'first'
            offsets = []
            trim = [0, 0, 0, 0]
        return offsets, blit_image, outline_size, trim

    # outlines image by creating mask from surface and blitting in certain directions
    def blit_outline(self, image, display, pos, outline_colour, offsets, edge_every):
        masks = pg.mask.from_surface(image).connected_components()
        for mask in masks:
            if offsets == [[0, 0]]:
                mask_outline = mask.outline(edge_every)
                mask_surface = pg.Surface(image.get_size())
                for pixel in mask_outline:
                    mask_surface.set_at(pixel, (255, 255, 255))
            else:
                mask_surface = mask.to_surface()
            mask_surface = self.palette_swap(mask_surface, (255, 255, 255), outline_colour)
            mask_surface.set_colorkey((0, 0, 0))
            for offset in offsets:
                display.blit(mask_surface, (pos[0] + offset[0], pos[1] + offset[1]))
        return display

    # trims unnecessary space around outline image
    def trim_outline(self, display, outline_size, trim):
        if outline_size:
            if trim[0]:
                display = display.subsurface((outline_size, 0, display.get_width() - outline_size, display.get_height()))
            if trim[1]:
                display = display.subsurface((0, 0, display.get_width() - outline_size, display.get_height()))
            if trim[2]:
                display = display.subsurface((0, outline_size, display.get_width(), display.get_height() - outline_size))
            if trim[3]:
                display = display.subsurface((0, 0, display.get_width(), display.get_height() - outline_size))
        return display

    def mask_get_at_range(self, mask, start, end=None):
        if not end:
            end = start
        for x in range(min(start[0], end[0]), max(start[0], end[0])):
            for y in range(min(start[0], end[0]), max(start[0], end[0])):
                if mask.get_at((x, y)):
                    return True
